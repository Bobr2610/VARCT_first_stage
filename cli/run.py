import os
import multiprocessing
import sys

from varkt.config import Config


def run_flight(config_):
    os.system(f'python flight.py {config_.data['flight_config']}')


def run_flight_plotter(config_):
    os.system(f'python flight_plotter.py {config_.data['flight_plotter_config']}')


def run_model_plotter(config_):
    os.system(f'python model_plotter.py {config_.data['model_plotter_config']}')


def run_analysis_plotter(config_):
    os.system(f'python analysis_plotter.py {config_.data['analysis_plotter_config']}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Нет имени файла конфигурации!')

    config = Config.from_file(sys.argv[1])

    flight_process = multiprocessing.Process(target=run_flight, args=(config,))
    flight_plotter_process = multiprocessing.Process(target=run_flight_plotter, args=(config,))
    model_plotter_process = multiprocessing.Process(target=run_model_plotter, args=(config,))
    analysis_plotter_process = multiprocessing.Process(target=run_analysis_plotter, args=(config,))

    print('Начало работы загрузчика')

    print('Запуск полёта')

    flight_process.start()

    print('Моделирование графиков полёта')

    flight_plotter_process.start()

    print('Моделирование графиков модели')

    model_plotter_process.start()

    print('Ожидание моделирования графиков полёта и модели')

    flight_process.join()
    flight_plotter_process.join()
    model_plotter_process.join()

    print('Моделирования графиков полёта и модели завершено')

    print('Моделирование графиков погрешностей и различий')

    analysis_plotter_process.start()

    print('Ожидание моделирования графиков погрешностей и различий')

    analysis_plotter_process.join()

    print('Моделирование графиков погрешностей и различий завершено')

    print('Окончание работы загрузчика')
