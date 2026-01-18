from logging.config import fileConfig
import os
from dotenv import load_dotenv
load_dotenv()
import asyncio
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from DataBase.TableModels.Base import Base
from DataBase.TableModels.CompaniesDbTableModel import CompaniesDbTableModel
from DataBase.TableModels.UserDbTableModel import UserDbTableModel
from DataBase.TableModels.RegistrationsDbTableModel import RegistrationsDbTableModel
from DataBase.TableModels.CompanyEmployeesDbTableModel import CompanyEmployeesDbTableModel
from DataBase.TableModels.Vehicles.CompanyVehiclesDbTableModel import CompanyVehiclesDbTableModel
from DataBase.TableModels.Vehicles.VehicleBodyTypesDbTableModel import VehicleBodyTypesDbTableModel
from DataBase.TableModels.Vehicles.VehicleLoadingTypesDbTableModel import VehicleLoadingTypesDbTableModel
from DataBase.TableModels.Vehicles.VehicleAdditionalOptionsDbTableModel import VehicleAdditionalOptionsDbTableModel

# Alembic config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Wszystkie modele w metadata
target_metadata = Base.metadata

# Offline
def run_migrations_offline():
    url = os.getenv("DB_CONNECTION_STRING", config.get_main_option("sqlalchemy.url"))
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# Online
def run_migrations_online():
    url = os.getenv("DB_CONNECTION_STRING", config.get_main_option("sqlalchemy.url"))
    if not url:
        raise RuntimeError("DB_CONNECTION_STRING not set")
    
    connectable = create_async_engine(url, poolclass=pool.NullPool)

    async def do_run_migrations():
        async with connectable.connect() as connection:
            # tutaj wywołujesz run_sync z funkcją synchroniczną
            def do_migrations(sync_conn):
                context.configure(connection=sync_conn, target_metadata=target_metadata)
                with context.begin_transaction():
                    context.run_migrations()
            
            await connection.run_sync(do_migrations)

    asyncio.run(do_run_migrations())

# Wybór trybu
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
