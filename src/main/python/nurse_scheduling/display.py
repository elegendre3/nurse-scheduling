from pathlib import Path

import pandas as pd
from IPython.display import (display, HTML)


def example():
    # creating the dataframe
    df = pd.DataFrame({
        "Name": ['Anurag', 'Manjeet', 'Shubham', 'Saurabh', 'Ujjawal'],
        "Address": ['Patna', 'Delhi', 'Coimbatore', 'Greater noida', 'Patna'],
        "ID": [20123, 20124, 20145, 20146, 20147],
        "Sell": [140000, 300000, 600000, 200000, 600000]
    })

    print("Original DataFrame :")
    display(df)

    print(df.to_html())


def csv_to_html(source_path: Path, target_path: Path):
    df = pd.read_csv(source_path)
    page = """<!DOCTYPE html>
<html lang="en" class="h-100">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <title>Schedule</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="style.css">
    <body>
        <header>
            <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
                <a class="navbar-brand" href="#">Nurse Scheduling</a>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarCollapse">
                <ul class="navbar-nav mr-auto">
                  <li class="nav-item"><a class="nav-link active" href="./overview">Overview</a></li>
                  <li class="nav-item"><a class="nav-link" href="./monday">Monday</a></li>
                  <li class="nav-item"><a class="nav-link" href="./tuesday">Tusday</a></li>
                  <li class="nav-item"><a class="nav-link" href="./wednesday">Wednesday</a></li>
                  <li class="nav-item"><a class="nav-link" href="./thursday">Thursday</a></li>
                  <li class="nav-item"><a class="nav-link" href="./friday">Friday</a></li>
                </ul>
                </div>
            </nav>
        </header>
        <div class="container">
            <br>
            <h1 class="mt-5">Weekly Schedule</h1>
            <br>
            {SCHEDULE_HERE}
        </div>
    </body>
</html>"""
    page_html = page.replace("{SCHEDULE_HERE}", df.to_html(classes='styled-table'))

    with target_path.open('w') as f:
        f.write(page_html)


if __name__ == "__main__":
    s_path = Path('../../scripts/schedule_[0].csv')
    t_path = Path('../../scripts/test.html')

    csv_to_html(s_path, t_path)
