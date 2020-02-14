import subprocess


def main():
    '''
    Calls xspider to scrape and save data, then plots this data using
    xspider_datahandler.py
    '''
    subprocess.run(['python3', 'xspider.py'])
    subprocess.run(['python3', 'xspider_datahandler.py'])


if __name__ == '__main__':
    main()
