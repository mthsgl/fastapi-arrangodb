from fastapi import APIRouter, Body, Request, HTTPException, status, Response
from typing import List
from models import Artist, ArtistUpdate

router = APIRouter()

@router.post("/", response_description="Create an artist", status_code=status.HTTP_201_CREATED, response_model=Artist)
def create_artist(request: Request, artist: Artist = Body(...)):
    collection = request.app.database["artists"]
    
    artist_dict = artist.dict(by_alias=True)
    if artist_dict.get("_key") is None:
        del artist_dict["_key"]
    
    try:
        doc = collection.createDocument(artist_dict)
        doc.save()
        return Artist(**doc.getStore())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_description="List all artists", response_model=List[Artist])
def list_artists(request: Request):
    collection = request.app.database["artists"]
    artists = [Artist(**doc.getStore()) for doc in collection.fetchAll()]
    return artists

@router.get("/{id}", response_description="Get a single artist by id", response_model=Artist)
def find_artist(id: str, request: Request):
    collection = request.app.database["artists"]
    try:
        doc = collection[id]
        return Artist(**doc.getStore())
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Artist with ID {id} not found")

@router.put("/{id}", response_description="Update an artist", response_model=Artist)
def update_artist(id: str, request: Request, artist: ArtistUpdate = Body(...)):
    collection = request.app.database["artists"]
    try:
        doc = collection[id]
        update_data = artist.dict(exclude_unset=True)
        
        for key, value in update_data.items():
            doc[key] = value
        
        doc.save()
        return Artist(**doc.getStore())
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Artist with ID {id} not found")

@router.delete("/{id}", response_description="Delete an artist")
def delete_artist(id: str, request: Request, response: Response):
    collection = request.app.database["artists"]
    try:
        doc = collection[id]
        doc.delete()
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Artist with ID {id} not found")