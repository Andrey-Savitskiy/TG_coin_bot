import aiosqlite


class SQLCommands:
    async def _fetchone(self, sql: str):
        db = await aiosqlite.connect('sqlite.db')
        cursor = await db.execute(sql)
        row = await cursor.fetchone()
        await cursor.close()
        await db.close()
        return row


    async def _fetchall(self, sql: str):
        db = await aiosqlite.connect('sqlite.db')
        cursor = await db.execute(sql)
        rows = await cursor.fetchall()
        await cursor.close()
        await db.close()
        return rows


    async def insert(self, table: str, columns: list, values: list):
        result_values = [f'"{item}"' if isinstance(item, str) else str(item) for item in values]
        sql = f"""
        INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(result_values)});
        """
        db = await aiosqlite.connect('sqlite.db')
        await db.execute(sql)
        await db.commit()
        await db.close()


    async def remove(self, table: str, id: int):
        sql = f"""
        DELETE FROM {table} WHERE id = {id}
        """
        db = await aiosqlite.connect('sqlite.db')
        await db.execute(sql)
        await db.commit()
        await db.close()

    async def select_coin(self, top: int):
        sql = f"""
        SELECT * FROM coins_data WHERE top = {top}
        """
        return await self._fetchall(sql)

    async def select_alerts(self):
        sql = f"""
        SELECT * FROM alert
        """
        return await self._fetchall(sql)

    async def select_password(self, password: str):
        sql = f"""
        SELECT id FROM user WHERE password = {password}
        """
        return await self._fetchone(sql)

    async def select_user(self, tg_id: int):
        sql = f"""
        SELECT id FROM user WHERE tg_id = {tg_id}
        """
        return await self._fetchone(sql)


commands = SQLCommands()
