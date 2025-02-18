from app.database import engine
import app.models

print("Creating database tables...")
app.models.Base.metadata.create_all(bind=engine)
print("Database setup complete.")
