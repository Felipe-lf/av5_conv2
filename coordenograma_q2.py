import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

def get_motor_starting_current(t_points, i_start, i_nominal, t_start):
    """Modela a curva de envelope da corrente de partida do motor."""
    decay_constant = t_start / 5
    current_envelope = (i_start - i_nominal) * np.exp(-t_points / decay_constant) + i_nominal
    current_envelope[t_points > t_start] = i_nominal
    return current_envelope

def get_weg_mpw_trip_curve(i_nominal):
    """Retorna os dados da curva de disparo real para a série WEG MPW."""
    thermal_multiples = np.array([1.15, 1.25, 1.5, 2.0, 3.0, 5.0, 7.8, 13.0])
    thermal_times_s = np.array([3600, 600, 120, 40, 15, 8, 5, 3.5])
    
    magnetic_multiple_trip = 13.5
    magnetic_currents_pu = np.array([magnetic_multiple_trip, 30])
    magnetic_times_s = np.array([0.02, 0.015])

    return {
        'thermal_currents': thermal_multiples * i_nominal,
        'thermal_times': thermal_times_s,
        'magnetic_currents': magnetic_currents_pu * i_nominal,
        'magnetic_times': magnetic_times_s
    }

def get_motor_withstand_curve(data_points_pu, i_nominal):
    """Extrai e converte os pontos da curva de suportabilidade do motor."""
    currents_pu, times_s = zip(*data_points_pu)
    currents_a = np.array(currents_pu) * i_nominal
    return np.array(times_s), currents_a


def plot_coordination_graph(params, motor_data, protection_data, withstand_data):
    """Gera e salva o gráfico de coordenograma de proteção do motor."""
    fig, ax = plt.subplots(figsize=(15, 10))
    
    ax.plot(withstand_data['times_cold'], withstand_data['currents_cold'], 'g^-', 
            label='Limite Térmico do Motor (Frio)', markersize=8, linewidth=2.5)
    ax.plot(withstand_data['times_hot'], withstand_data['currents_hot'], 'bo-', 
            label='Limite Térmico do Motor (Quente)', markersize=8, linewidth=2.5, alpha=0.7)

    ax.plot(protection_data['thermal_times'], protection_data['thermal_currents'], 'r--', 
            label='Curva de Disparo (WEG MPW80)', linewidth=2.5)
    
    ax.plot(motor_data['times'], motor_data['currents'], 'k-', 
            label='Corrente de Partida do Motor', linewidth=3, alpha=0.8)

    ax.axvline(x=params['t_start'], color='darkgreen', linestyle=':', linewidth=2, 
                label=f'Tempo de Partida ({params["t_start"]}s)')
    
    ax.axvline(x=params['t_lrc_cold'], color='darkred', linestyle=':', linewidth=2, 
                label=f'Tempo de Rotor Bloqueado ({params["t_lrc_cold"]}s)')

    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.set_title('Coordenograma de Proteção e Partida do Motor', fontsize=20, fontweight='bold')
    ax.set_xlabel('Tempo (s) - [Escala Log]', fontsize=14)
    ax.set_ylabel('Corrente (A) - [Escala Log]', fontsize=14)
    ax.legend(fontsize=12)
    ax.grid(True, which="both", ls="-", color='0.85')
    
    ax.set_xlim(0.1, 1000)
    ax.set_ylim(params['i_nominal'] * 0.9, params['i_start_peak'] * 2)

    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_formatter(ScalarFormatter())
    
    plt.savefig('coordenograma_tempo_x_corrente.png', dpi=300)
    plt.show()

if __name__ == '__main__':
    
    SIMULATION_PARAMS = {
        't_start': 0.75,
        't_lrc_cold': 27.0,
        'i_start_peak': 820.0,
        'i_nominal': 61.9,
    }

    WEG_COLD_CURVE_DATA = [(2.0, 1200), (2.5, 450), (3.0, 250), (4.0, 80), (5.0, 50), (6.0, 40), (7.8, 27)]
    WEG_HOT_CURVE_DATA = [(2.5, 55), (3.0, 50), (4.0, 30), (5.0, 20), (6.0, 15), (7.0, 11), (7.8, 9)]
    
    time_points = np.linspace(0.01, SIMULATION_PARAMS['t_lrc_cold'] + 5, 2000)
    
    motor_current_values = get_motor_starting_current(
        t_points=time_points,
        i_start=SIMULATION_PARAMS['i_start_peak'],
        i_nominal=SIMULATION_PARAMS['i_nominal'],
        t_start=SIMULATION_PARAMS['t_start']
    )
    
    protection_curve_data = get_weg_mpw_trip_curve(i_nominal=SIMULATION_PARAMS['i_nominal'])
    
    withstand_t_cold, withstand_i_cold = get_motor_withstand_curve(
        data_points_pu=WEG_COLD_CURVE_DATA,
        i_nominal=SIMULATION_PARAMS['i_nominal']
    )

    withstand_t_hot, withstand_i_hot = get_motor_withstand_curve(
        data_points_pu=WEG_HOT_CURVE_DATA,
        i_nominal=SIMULATION_PARAMS['i_nominal']
    )

    plot_coordination_graph(
        params=SIMULATION_PARAMS,
        motor_data={'times': time_points, 'currents': motor_current_values},
        protection_data=protection_curve_data,
        withstand_data={
            'times_cold': withstand_t_cold,
            'currents_cold': withstand_i_cold,
            'times_hot': withstand_t_hot,
            'currents_hot': withstand_i_hot
        }
    )

    print("Gráfico 'coordenograma_tempo_x_corrente.png' foi salvo com sucesso.")