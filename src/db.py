from twisted.enterprise import adbapi
import config

dbpool = adbapi.ConnectionPool(config.DB_MODULE, database=config.DB_BASE, user=config.DB_USER, host=config.DB_HOST, password=config.DB_PASS)
