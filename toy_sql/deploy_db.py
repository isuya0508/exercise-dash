from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

import database
from database import db_path, session_scope


def fetch_csv() -> pd.DataFrame:
    """csvをリポジトリから取得する

    Returns
    -------
    pandas.DataFrame
    """

    csv_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/flags/flag.data'
    csv_attributes = [
        'name', 'landmass', 'zone', 'area', 'population', 'language', 'religion',
        'bars', 'stripes', 'colours', 'red', 'green', 'blue', 'gold', 'white', 'black', 'orange',
        'mainhue', 'circles', 'crosses', 'saltires', 'quarters', 'sunstars', 'crescent', 'triangle',
        'icon', 'animate', 'text', 'topleft', 'botright'
    ]
    df = pd.read_csv(csv_url, header=None, names=csv_attributes)

    return df


def load_csv() -> pd.DataFrame:
    """csvを取得する

    .data/flags.csvが存在する場合はそのcsvを読み込み、存在しない場合はcsvを
    リポジトリから取得した後、.data/flags.csvとして保存する。

    Returns
    -------
    pandas.DataFrame
    """

    csv_dir = Path(__file__).with_name('data')
    csv_path = csv_dir / 'flags.csv'

    if csv_path.exists():
        df = pd.read_csv(csv_path)

    else:
        df = fetch_csv()

        csv_dir.mkdir(exist_ok=True)
        df.to_csv(csv_path, index=False)

    return df


def main():
    """.data/db.sqliteにSQLite DBをデプロイする

    DBテーブルを作成し、dfからデータを生成して各テーブルに挿入する。
    """

    if not db_path.parent.exists():
        db_path.parent.mkdir()

    if db_path.exists():
        db_path.unlink()

    engine = create_engine(f'sqlite:///{db_path}', echo=True)
    database.create_db(engine)

    df = load_csv()

    countries = [
        database.Country(
            name=r.name,
            landmass_id=r.landmass,
            zone_id=r.zone,
            area=r.area,
            population=r.population,
            language_id=r.language,
            religion_id=r.religion
        )
        for r in df.itertuples()
    ]
    landmasses = [
        database.Landmass(id=1, name='N.America'),
        database.Landmass(id=2, name='S.America'),
        database.Landmass(id=3, name='Europe'),
        database.Landmass(id=4, name='Africa'),
        database.Landmass(id=5, name='Asia'),
        database.Landmass(id=6, name='Oceania'),
    ]
    zones = [
        database.Zone(id=1, quadrant='NE'),
        database.Zone(id=2, quadrant='SE'),
        database.Zone(id=3, quadrant='SW'),
        database.Zone(id=4, quadrant='NW')
    ]
    languages = [
        database.Language(id=1, name='English'),
        database.Language(id=2, name='Spanish'),
        database.Language(id=3, name='French'),
        database.Language(id=4, name='German'),
        database.Language(id=5, name='Slavic'),
        database.Language(id=6, name='Other Indo-European'),
        database.Language(id=7, name='Chinese'),
        database.Language(id=8, name='Arabic'),
        database.Language(id=9, name='Japanese/Turkish/Finnish/Magyar'),
        database.Language(id=10, name='Others'),
    ]
    religions = [
        database.Religion(id=0, name='Catholic'),
        database.Religion(id=1, name='Other Christian'),
        database.Religion(id=2, name='Muslim'),
        database.Religion(id=3, name='Buddhist'),
        database.Religion(id=4, name='Hindu'),
        database.Religion(id=5, name='Ethnic'),
        database.Religion(id=6, name='Marxist'),
        database.Religion(id=7, name='Others')
    ]

    with session_scope(engine) as session:
        session.add_all(countries)
        session.add_all(landmasses)
        session.add_all(zones)
        session.add_all(languages)
        session.add_all(religions)


if __name__ == '__main__':
    main()
