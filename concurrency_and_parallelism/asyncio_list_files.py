import asyncio
import glob

folder = "/Users/j35/Desktop/test_output/test/"

async def main():
    """
    This program looks for new files in the folder and then will stop when 6 files have been found!
    Ideally, the stop parameter will come from outside
    """
    list_files = []
    print("Looking at new files in that folder")
    is_continue = True
    while is_continue:
        full_list_files = glob.glob(folder + "*.tiff")
        if len(full_list_files) > len(list_files):
            for _file in full_list_files:
                if not (_file in list_files):
                    print(f"-> new file: {_file}")
                    list_files.append(_file)
        elif len(list_files) == 6:
            return 
        else:
            await asyncio.sleep(2)

    
asyncio.run(main())


