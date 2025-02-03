from dotenv import load_dotenv # type: ignore

load_dotenv(dotenv_path='.env')
load_dotenv(dotenv_path='.env.local', override=True)