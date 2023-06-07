from fastapi import APIRouter, HTTPException, Body, Request, Response, status
from . import models
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/main",
    tags=["main"],
    responses={404: {"description": "Not found"}},
)

# -----------------------------------------------------------------------------------------------------------------------

@router.get("/user", response_description="List all users", response_model=list[models.User])
async def list_users(request: Request):
    user = list(request.app.database["users"].find(limit=100))
    return user

#@router.get("/user/{userid}", response_description="Get user information by id", response_model=models.User)
#async def get_user_info(userid: str, request: Request):
#    if (user := request.app.database["users"].find_one({"_id": userid})) is not None:
#        return user
#    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {userid} not found")

@router.get("/user/{username}", response_description="Get user id and email by username", response_model=models.UserResponse)
async def get_user_id_email_by_username(username: str, request: Request):

    if (user := request.app.database["users"].find_one({"username": username})) is not None:
        response = models.UserResponse(id=user['_id'],email=user['email'])

        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with Username {username} not found")

@router.get("/user/idemail/{username}", response_description="Get user information by username", response_model=models.UserResponse2)
async def get_user_info_by_username(username: str, request: Request):

    if (user := request.app.database["users"].find_one({"username": username})) is not None:
        response = models.UserResponse2(
            name=user['name'],
            email=user['email'],
            phoneNumber=user['phoneNumber'],
            address=user['address']
        )

        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with Username {username} not found")

@router.put("/user/{userid}", response_description="Update a User", response_model=models.User)
async def put_user(userid: str, request: Request, user: models.UserUpdate = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}
    if len(user) >= 1:
        update_result = request.app.database["users"].update_one(
            {"_id": userid}, {"$set": user}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {userid} not found")

    if (
        user := request.app.database["users"].find_one({"_id": userid})
    ) is not None:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {userid} not found")

@router.post("/user")
async def post_user(request: Request, user: models.User = Body(...)):
    user = jsonable_encoder(user)
    new_user = request.app.database["users"].insert_one(user)
    user = request.app.database["users"].find_one(
        {"_id": new_user.inserted_id}
    )

    return user

@router.delete("/user/{userid}", response_description="Delete a User")
async def delete_user(userid: str, request: Request, response: Response):
    delete_result = request.app.database["users"].delete_one({"_id": userid})
    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {userid} not found")

# -----------------------------------------------------------------------------------------------------------------------

@router.get("/drivers", response_description="List all drivers", response_model=list[models.Driver])
async def list_driver(request: Request):
    driver = list(request.app.database["drivers"].find(limit=100))
    return driver

@router.get("/driver", response_description="List all drivers info (some)", response_model=list[models.DriverResponse])
async def list_driver_info(request: Request):
    drivers = list(request.app.database["drivers"].find(limit=100))
  
    response = [models.DriverResponse(
        id=driver['_id'],
        name=driver['name'],
        licence_plate=driver['licence_plate'],
        car_model=driver['car_model'],
        coordenates=driver['coordenates']
    ) for driver in drivers]

    return response

@router.get("/driver/byid/{driverid}", response_description="List driver by id", response_model=models.DriverResponse3)
async def get_driver_info_by_id(driverid: str, request: Request):

    if (driver := request.app.database["drivers"].find_one({"_id": driverid})) is not None:
        response = models.DriverResponse3(name=driver['name'],email=driver['email'],phoneNumber=driver['phoneNumber'])

        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {driverid} not found")


@router.get("/driver/answers", response_description="List all driver answers", response_model=list[models.DriverResponse2])
async def list_driver_info(request: Request):
    drivers = list(request.app.database["drivers"].find(limit=100))
  
    response = [models.DriverResponse2(
        id=driver['_id'],
        answer1=driver['answer1'],
        answer2=driver['answer2'],
        answer3=driver['answer3'],
    ) for driver in drivers]

    return response


@router.post("/driver")
async def post_driver(request: Request, user: models.Driver = Body(...)):
    driver = jsonable_encoder(user)
    new_driver = request.app.database["drivers"].insert_one(driver)
    driver = request.app.database["drivers"].find_one(
        {"_id": new_driver.inserted_id}
    )

    return user

@router.delete("/driver/{driverid}", response_description="Delete a Driver")
async def delete_driver(driverid: str, request: Request, response: Response):
    delete_result = request.app.database["drivers"].delete_one({"_id": driverid})
    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {driverid} not found")

# -----------------------------------------------------------------------------------------------------------------------

@router.get("/trips", response_description="List all Trips", response_model=list[models.Trip])
async def list_trips(request: Request):
    trips = list(request.app.database["trips"].find(limit=100))
    return trips

@router.post("/trip")
async def post_trip(request: Request, trip: models.Trip = Body(...)):
    trip = jsonable_encoder(trip)

    if (request.app.database["drivers"].find_one({"_id": trip["driverId"]})) is not None:
        if (request.app.database["users"].find_one({"username": trip["username"]})) is not None:

            new_trip = request.app.database["trips"].insert_one(trip)
            created_trip = request.app.database["trips"].find_one(
                {"_id": new_trip.inserted_id}
            )

            return created_trip
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User  not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Driver not found")

# -----------------------------------------------------------------------------------------------------------------------

@router.get("/payment", response_description="List all payments", response_model=list[models.Payment])
async def list_payments(request: Request):
    trips = list(request.app.database["payment"].find(limit=100))
    return trips

@router.post("/payment")
async def post_payment(request: Request, payment: models.Payment = Body(...)):
    payment = jsonable_encoder(payment)

    if (request.app.database["trips"].find_one({"_id": payment["travelId"]})) is not None:
        if (request.app.database["users"].find_one({"username": payment["username"]})) is not None:
            new_payment = request.app.database["payment"].insert_one(payment)
            created_payment = request.app.database["payment"].find_one(
                {"_id": new_payment.inserted_id}
            )

            return created_payment
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User  not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip not found")