import aiomysql
import asyncio

async def async_dbConnect_query(sqlCommand, params1, many=False):
    mysql_db_ip = "172.16.1.103"
    
    # 創建連接池
    pool = await aiomysql.create_pool(
        host=mysql_db_ip,
        user="root",
        password="1qaz@WSX",
        db="DoorSecurity",
        port=13306,
        autocommit=False
    )
    
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            try:
                if many:
                    await cursor.executemany(sqlCommand, params1)
                else:
                    await cursor.execute(sqlCommand, params1)
                await conn.commit()
            except Exception as e:
                await conn.rollback()
                print(f"Database error: {e}")
                raise
    
    pool.close()
    await pool.wait_closed()