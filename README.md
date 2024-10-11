# Email-Genie

the zipfile of the docker app can be accessed at this drive link : [https://drive.google.com/file/d/1eE9NS08gfMAfHqijyYUqc82qKKa2kBJq/view?usp=drive_link](https://drive.google.com/file/d/1bsT3woolBfPsQPR3S47vsAz7596uTgOf/view?usp=drive_link)
we were unable to add the full dockerized zip to the repo due to github constraints and our file size exceeding the size limits. 

Once you have unzipped the zipfile and entered the terminal in the app folder, run the folllowing commands
1. docker build -t emailgenie .
2. docker run -p 8501:8501 -e GROQ_API_KEY=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 emailgenie

this should lead to the app running on your localhost, where you can test it out.

a video demo can be seen here: https://drive.google.com/file/d/1eE9NS08gfMAfHqijyYUqc82qKKa2kBJq/view?usp=drive_link
