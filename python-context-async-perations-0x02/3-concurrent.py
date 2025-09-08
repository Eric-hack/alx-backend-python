import asyncio
import aiosqlite


async def async_fetch_users(db_file="users.db"):
    """Fetch all users asynchronously"""
    async with aiosqlite.connect(db_file) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users(db_file="users.db"):
    """Fetch users older than 40 asynchronously"""
    async with aiosqlite.connect(db_file) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()


async def fetch_concurrently():
    """Run both queries concurrently"""
    all_users, older_users = await asyncio.gather(
        async_fetch_users(), async_fetch_older_users()
    )

    print(" All Users:")
    for user in all_users:
        print(user)

    print("\n Users Older than 40:")
    for user in older_users:
        print(user)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
