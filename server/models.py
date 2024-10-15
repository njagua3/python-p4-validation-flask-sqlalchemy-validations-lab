from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name', 'phone_number')
    def validate_fields(self, key, value):
        # Validate name
        if key == 'name':
            if not value:
                raise ValueError("Author must have a name.")
            if len(value) < 2:
                raise ValueError("Author's name must be at least 2 characters long.")
            # Check for uniqueness
            if db.session.query(Author).filter_by(name=value).first():
                raise ValueError(f"Author name '{value}' is already taken.")
            return value
        
        # Validate phone number: must be exactly 10 digits
        if key == 'phone_number':
            if value and (len(value) != 10 or not value.isdigit()):
                raise ValueError("Phone number must be exactly 10 digits.")
            return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)  # Ensure content is required
    category = db.Column(db.String, nullable=False)  # Category is required
    summary = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title', 'content', 'summary', 'category')
    def validate_fields(self, key, value):
        if key == 'title':
            # Check for clickbait titles
            if not value or len(value) < 5:  # Optional: Minimum length for titles
                raise ValueError("Title must be at least 5 characters long.")
            clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
            if not any(keyword in value for keyword in clickbait_keywords):
                raise ValueError("Title must contain one of the following: 'Won't Believe', 'Secret', 'Top', 'Guess'.")
            return value

        if key == 'content':
            if not value or len(value) < 250:  # Content must be at least 250 characters
                raise ValueError("Content must be at least 250 characters long.")
            return value
        
        if key == 'summary':
            if value and len(value) > 250:  # Summary must be a maximum of 250 characters
                raise ValueError("Summary must be 250 characters or less.")
            return value

        if key == 'category':
            # Category must be either 'Fiction' or 'Non-Fiction'
            if value not in ["Fiction", "Non-Fiction"]:
                raise ValueError("Category must be either 'Fiction' or 'Non-Fiction'.")
            return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'
