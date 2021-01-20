# get_HouseProperties
API endpoint which obtains the requested property info of a house/apartment/building

## List of Endpoints
### localhost:8000/api/provider/ and localhost:8000/api/fields/:
These are the endpoints for the CRUD operations for the models Provider and Fields.
#### POST Body Format for provider:

  {
            "id": numeric,
            "name": name_of_provider,
            "url": url_of_provider,
            "priority": numeric between 1 to 9,
            "created_at":date_time_format
    }
    
    Note: The priority has to be a number between 1 and 9, 1 being the highest priority and 9 the lowest
  
{
        "id": numeric,
        "name": name of the field in the provider API,
        "key_phrase": name of the field on the answers endpoint,
        "provider": numeric, ID of the provider
    }
    
  
  ### localhost:8000/api/answers
  Endpoint to obtain the desired property of a house/apartment/building (refered for now on as house)
  **These are the required parameters**
  - address: number and street of house
  - zipcode: zipcode of house location
  - key_phrase: Property to search on the 3erd party api. The allow one:
    - air_conditioning: 
    - attic:
    - basement
    - building_area_sq_ft:
    - building_condition_score:
    - building_quality_score:
    - construction_type:
    - exterior_walls:
    - fireplace:
    - full_bath_count:
    - garage_parking_of_cars:
    - garage_type_parking:
    - heating:
    - heating_fuel_type:
    - no_of_buildings:
    - no_of_stories:
    - number_of_bedrooms:
    - number_of_units:
    - partial_bath_count:
    - pool:
    - property_type:                 
    - roof_cover:
    - roof_type:
    - site_area_acres:
    - style:
    - total_bath_count:
    - total_number_of_rooms:
    - sewer:
    - subdivision:
    - water:
    - year_built:
    - zoning:
  
