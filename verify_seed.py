import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from src.config.db import init_db, get_session
from src.generator.models import Role
from sqlmodel import select


async def main():
    print('Starting verification...')
    try:
        await init_db()
        print('init_db completed.')

        # Check if roles exist
        gen = get_session()
        session = await gen.__anext__()

        roles = await session.exec(select(Role))
        results = roles.all()

        print(f'Found {len(results)} roles:')
        found_names = []
        for r in results:
            print(f'- {r.name}')
            found_names.append(r.name)

        if 'Manager' in found_names and 'user' in found_names:
            print('SUCCESS: Target roles found.')
        else:
            print('FAILURE: Target roles missing.')

    except Exception as e:
        print(f'Error: {e}')
        import traceback

        traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(main())
