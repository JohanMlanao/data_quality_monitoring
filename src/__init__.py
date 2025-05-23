from src.store import StoreSensor


def create_app() -> dict:

    store_location = ["Lille", "Paris", "Lyon", "Bordeaux", "Marseille"]
    store_avg_visit = [3000, 8000, 6000, 2000, 1700]
    store_std_visit = [500, 800, 500, 400, 100]
    perc_malfunction = [0.05, 0.1, 0.08, 0.05, 0.05]
    perc_break = [0.05, 0.08, 0.05, 0.02, 0]

    store_dict = dict()

    for i in range(len(store_location)):
        store_dict[store_location[i]] = StoreSensor(
            store_location[i],
            store_avg_visit[i],
            store_std_visit[i],
            perc_malfunction[i],
            perc_break[i],
        )
    return store_dict
