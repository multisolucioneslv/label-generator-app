import mysql.connector
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime
import bcrypt
from config import config

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    approved_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    approved_at = Column(DateTime, nullable=True)

    # Relationships
    labels = relationship("Label", back_populates="user")
    approved_users = relationship("User", remote_side=[id])

    def set_password(self, password):
        """Hash and set password"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        """Check if password matches"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class AppSetting(Base):
    __tablename__ = 'app_settings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    setting_key = Column(String(100), unique=True, nullable=False)
    setting_value = Column(Text)
    description = Column(Text)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

class Label(Base):
    __tablename__ = 'labels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Sender information
    sender_name = Column(String(100), nullable=False)
    sender_address = Column(Text, nullable=False)
    sender_city = Column(String(50), nullable=False)
    sender_state = Column(String(50), nullable=False)
    sender_zip = Column(String(20), nullable=False)

    # Recipient information
    recipient_name = Column(String(100), nullable=False)
    recipient_address = Column(Text, nullable=False)
    recipient_city = Column(String(50), nullable=False)
    recipient_state = Column(String(50), nullable=False)
    recipient_zip = Column(String(20), nullable=False)
    recipient_tracking = Column(String(100), nullable=True)

    # Label metadata
    label_type = Column(String(50), default='standard')
    status = Column(String(20), default='generated')
    notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    user = relationship("User", back_populates="labels")

class AuditLog(Base):
    __tablename__ = 'audit_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    action = Column(String(100), nullable=False)
    table_name = Column(String(50))
    record_id = Column(Integer)
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime, default=func.current_timestamp())

class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.connected = False

    def connect(self):
        """Connect to MySQL database"""
        try:
            # Test connection first
            connection = mysql.connector.connect(
                host=config.DB_HOST,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                port=config.DB_PORT
            )

            # Create database if it doesn't exist
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.DB_NAME}")
            cursor.close()
            connection.close()

            # Create SQLAlchemy engine
            self.engine = create_engine(config.DATABASE_URL, echo=config.DEBUG)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

            # Create tables
            Base.metadata.create_all(bind=self.engine)

            self.connected = True
            print(f"✅ Connected to MySQL database: {config.DB_NAME}")
            return True

        except Exception as e:
            print(f"❌ Database connection failed: {str(e)}")
            self.connected = False
            return False

    def get_session(self):
        """Get database session"""
        if not self.connected:
            if not self.connect():
                return None
        return self.SessionLocal()

    def create_admin_user(self):
        """Create default admin user if it doesn't exist"""
        try:
            session = self.get_session()
            if not session:
                return False

            # Check if admin user exists
            admin = session.query(User).filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@labelgenerator.com',
                    full_name='Administrator',
                    is_active=True,
                    is_admin=True
                )
                admin.set_password('123')  # Default password
                session.add(admin)
                session.commit()
                print("✅ Default admin user created (username: admin, password: 123)")

            session.close()
            return True

        except Exception as e:
            print(f"❌ Error creating admin user: {str(e)}")
            return False

    def get_setting(self, key, default=None):
        """Get application setting"""
        try:
            session = self.get_session()
            if not session:
                return default

            setting = session.query(AppSetting).filter_by(setting_key=key).first()
            session.close()

            return setting.setting_value if setting else default

        except Exception as e:
            print(f"❌ Error getting setting {key}: {str(e)}")
            return default

    def set_setting(self, key, value, description=None):
        """Set application setting"""
        try:
            session = self.get_session()
            if not session:
                return False

            setting = session.query(AppSetting).filter_by(setting_key=key).first()
            if setting:
                setting.setting_value = value
                if description:
                    setting.description = description
            else:
                setting = AppSetting(
                    setting_key=key,
                    setting_value=value,
                    description=description
                )
                session.add(setting)

            session.commit()
            session.close()
            return True

        except Exception as e:
            print(f"❌ Error setting {key}: {str(e)}")
            return False

# Global database manager instance
db_manager = DatabaseManager()