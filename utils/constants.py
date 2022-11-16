import geopandas as gpd
import geojson

MAP_SELECTION_COLOR = "purple"
MAP_MODEBAR_COLOR = "deeppink"
MAP_MODEBAR_COLOR_ACTIVE = "rgb(100,0,200)"
OIL_COLOR = "rgb(0,200,0)"
GAS_COLOR = "rgb(200,0,0)"

# Kansas Geometry Constants
KANSAS_STATE = gpd.read_file("utils/geometry/cb_2018_us_county_500k.shp")
KANSAS_STATE = KANSAS_STATE[KANSAS_STATE["STATEFP"] == "20"].reset_index(drop=True)
KANSAS_STATE["LSAD"] = KANSAS_STATE["LSAD"].astype(int)

# Kansas projection data
KANSAS_CRS = KANSAS_STATE.crs

# Kansas GeoJson of Geometry
with open("utils/geometry/kansas_counties.geojson") as f:
    KANSAS_GEOJSON = geojson.load(f)

# Kansas state GPS Midpoint
DEFAULT_MIDPOINT = (38.62470, -98.38020)

# Kansas default zoom level
DEFAULT_ZOOM = 6

# Kansas Counties
COUNTIES = sorted(
    [
        "Seward",
        "Grant",
        "Morton",
        "Finney",
        "Kearny",
        "Stevens",
        "Haskell",
        "Stanton",
        "Hamilton",
        "Wichita",
        "Bourbon",
        "Allen",
        "Anderson",
        "Crawford",
        "Chautauqua",
        "Elk",
        "Coffey",
        "Franklin",
        "Douglas",
        "Jackson",
        "Johnson",
        "Labette",
        "Leavenworth",
        "Linn",
        "Miami",
        "Marion",
        "Montgomery",
        "Nemaha",
        "Neosho",
        "Woodson",
        "Wilson",
        "Greenwood",
        "Brown",
        "Butler",
        "Sedgwick",
        "Cowley",
        "Chase",
        "Sumner",
        "Dickinson",
        "Lyon",
        "Morris",
        "Pottawatomie",
        "Geary",
        "Riley",
        "Wabaunsee",
        "Ellis",
        "Barton",
        "Rice",
        "Ellsworth",
        "Russell",
        "Stafford",
        "McPherson",
        "Harvey",
        "Saline",
        "Osborne",
        "Reno",
        "Barber",
        "Harper",
        "Kingman",
        "Pratt",
        "Hodgeman",
        "Comanche",
        "Clark",
        "Decatur",
        "Edwards",
        "Pawnee",
        "Rooks",
        "Trego",
        "Rush",
        "Ford",
        "Gove",
        "Graham",
        "Sheridan",
        "Kiowa",
        "Lane",
        "Logan",
        "Meade",
        "Ness",
        "Norton",
        "Phillips",
        "Rawlins",
        "Scott",
        "Thomas",
        "Sherman",
        "Gray",
        "Wallace",
        "Cheyenne",
        "Osage",
        "Greeley",
        "Jefferson",
        "Wyandotte",
        "Atchison",
        "Clay",
        "Marshall",
    ]
)


TIMEOUT = 60

YEAR_START = 1930
YEAR_END = 2022
