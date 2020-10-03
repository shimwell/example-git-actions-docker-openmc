
import openmc

class MinimalSimulation:
    """This is a dummy class that has a few tiny methods to demonstrate testing
    """

    def __init__(self):
        pass

    def simulate(self):
        """this runs a simple tbr simulation using openmc and returns the
        tritium breeding ratio"""

        breeder_material = openmc.Material(1, "PbLi")  # Pb84.2Li15.8
        breeder_material.add_element('Pb', 84.2, percent_type='ao')
        breeder_material.add_element('Li', 15.8, percent_type='ao', enrichment=50.0, enrichment_target='Li6', enrichment_type='ao')  # 50% enriched
        breeder_material.set_density('atom/b-cm', 3.2720171e-2)  # around 11 g/cm3


        mats = openmc.Materials([breeder_material])


        # GEOMETRY

        # surfaces
        vessel_inner = openmc.Sphere(r=500)
        breeder_blanket_outer_surface = openmc.Sphere(r=600, boundary_type='vacuum')

        # cells
        inner_vessel_region = -vessel_inner
        inner_vessel_cell = openmc.Cell(region=inner_vessel_region)

        breeder_blanket_region = -breeder_blanket_outer_surface
        breeder_blanket_cell = openmc.Cell(region=breeder_blanket_region)
        breeder_blanket_cell.fill = breeder_material

        # universe
        universe = openmc.Universe(cells=[inner_vessel_cell, breeder_blanket_cell])
        geom = openmc.Geometry(universe)


        # SIMULATION SETTINGS

        # Instantiate a Settings object
        sett = openmc.Settings()
        sett.batches = 2
        sett.inactive = 0
        sett.particles = 100
        sett.run_mode = 'fixed source'

        # Create a DT point source
        source = openmc.Source()
        source.space = openmc.stats.Point((0, 0, 0))
        source.angle = openmc.stats.Isotropic()
        source.energy = openmc.stats.Discrete([14e6], [1])
        sett.source = source

        tallies = openmc.Tallies()

        # added a cell tally for tritium production
        cell_filter = openmc.CellFilter(breeder_blanket_cell)
        tbr_tally = openmc.Tally(name='TBR')
        tbr_tally.filters = [cell_filter]
        tbr_tally.scores = ['(n,Xt)']  # MT 205 is the (n,Xt) reaction where X is a wildcard, if MT 105 or (n,t) then some tritium production will be missed, for example (n,nt) which happens in Li7 would be missed
        tallies.append(tbr_tally)

        # Run OpenMC!
        model = openmc.model.Model(geom, mats, sett, tallies)
        sp_filename = model.run()

        # open the results file
        sp = openmc.StatePoint(sp_filename)

        # access the tally using pandas dataframes
        tbr_tally = sp.get_tally(name='TBR')
        df = tbr_tally.get_pandas_dataframe()

        tbr_tally_result = df['mean'].sum()

        return tbr_tally_result
