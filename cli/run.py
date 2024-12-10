import os
import multiprocessing
import sys

from varkt.config import Config


def run_flight():
    os.system('python flight.py')


def run_flight_plotter(config_):
    os.system(f'python flight_plotter.py {config_.data['flight_plotter_config']}')


def run_model_plotter(config_):
    os.system(f'python model_plotter.py {config_.data['model_plotter_config']}')


def run_inaccuracy_plotter(config_):
    os.system(f'python inaccuracy_plotter.py {config_.data['inaccuracy_plotter_config']}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Нет имени файла конфигурации!')

    config = Config.from_file(sys.argv[1])

    flight_process = multiprocessing.Process(target=run_flight)
    flight_plotter_process = multiprocessing.Process(target=run_flight_plotter, args=(config,))
    model_plotter_process = multiprocessing.Process(target=run_model_plotter, args=(config,))
    inaccuracy_plotter_process = multiprocessing.Process(target=run_inaccuracy_plotter, args=(config,))

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

    print('Моделирование графиков погрешностей')

    inaccuracy_plotter_process.start()

    print('Ожидание моделирования графиков погрешностей')

    inaccuracy_plotter_process.join()

    print('Моделирование графиков погрешностей завершено')

    print('Окончание работы загрузчика')
