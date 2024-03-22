# l={
  
# }

# n:int=int(input("the peron number want  go to:"))

# for i in range(1,n+1):
   
#     l.update({f"person{i}":int(input(f"balance of person{i} is:"))})
    
# cost=input("input cost and put a space ").split(" ")

# totalcost=sum([int(i) for i in cost])

# perhead=totalcost/n

# perhead=round(perhead,2)

# for i in l:
#     if l[i]<perhead:
#         print(f"{i} has to pay {perhead-l[i]}")
#     else:
#         print(f"{i} will get {l[i]-perhead}")


# def replay(text)->str:
#   if text=="hi":
#     return "hello"
#   elif text=="how are you":
#     return "I am fine"
#   elif text=="bye":
#     return "bye"
#   elif text=="what is your name":
#     return "I am chatbot"
#   elif text=="Do you know me?":
#     return "You are from Daffodil International University.blah blah blah"

  
  
  


# def chatGt()->None:
#   while True:
#     text=input("You: ").lower()
#     if text=="bye":
#       print("Chatbot: bye")
#       break
#     print(f"Chatbot: {replay(text)}")

# if __name__=="__main__":
#   chatGt()

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# Replace with your actual values
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")  # Configure token endpoint

# Define a model for user data (optional)
class User(BaseModel):
  user_id: str
  # Add other relevant user information

# Dependency for verifying JWT token
async def get_current_user(token: str = Depends(oauth2_scheme)):
  # Validate token using Auth0 library (not included here)
  # Raise exception for invalid token
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
  )
  # Replace with your validation logic using Auth0 library
  # user = validate_token(token)  # Hypothetical validation function
  raise credentials_exception  # Placeholder for now

app = FastAPI()

@app.get("/authorized")
async def secured_resource(current_user: User = Depends(get_current_user)):
  # Access user information from current_user object (if defined in model)
  # return {"message": f"Welcome, {current_user.user_id}!"}  # Example with user data
  return {"message": "Secured Resource"}

if __name__=="__main__":
  import uvicorn
  uvicorn.run(app, host="localhost", port=8000)