```python

import numpy as np
import random
import logging
from dataclasses import dataclass
from typing import List, Tuple
import json
from datetime import datetime

@dataclass
class IterationLog:
    """Clase para almacenar los logs de cada iteración"""
    iteration: int
    weights: List[float]
    bias: float
    total_error: int
    steps: List[dict]

class PerceptronLogger:
    """Clase para manejar el logging del perceptrón"""
    def __init__(self, log_file: str = None):
        self.logs = []
        self.log_file = log_file or f"perceptron_training_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
    def add_iteration(self, log: IterationLog):
        self.logs.append({
            "iteration": log.iteration,
            "weights": [round(w, 3) for w in log.weights],
            "bias": round(log.bias, 3),
            "total_error": log.total_error,
            "steps": log.steps
        })
    
    def save(self):
        """Guarda los logs en un archivo JSON"""
        with open(self.log_file, 'w') as f:
            json.dump(self.logs, f, indent=2)
    
    def get_summary(self) -> str:
        """Genera un resumen del entrenamiento"""
        if not self.logs:
            return "No hay logs disponibles"
        
        first_iter = self.logs[0]
        last_iter = self.logs[-1]
        return (
            f"Entrenamiento completado en {len(self.logs)} iteraciones\n"
            f"Pesos iniciales: {first_iter['weights']}, Bias inicial: {first_iter['bias']}\n"
            f"Pesos finales: {last_iter['weights']}, Bias final: {last_iter['bias']}\n"
            f"Error final: {last_iter['total_error']}"
        )

class Perceptron:
    def __init__(self, n_inputs: int):
        self.weights = [random.uniform(-1, 1) for _ in range(n_inputs)]
        self.bias = random.uniform(-1, 1)
        self.logger = PerceptronLogger()

    def activation(self, weighted_sum: float) -> int:
        return 1 if weighted_sum > 0 else 0

    def train(self, 
              inputs: List[Tuple], 
              labels: List[int], 
              max_iterations: int = 1000, 
              learning_rate: float = 0.1) -> Tuple[List[float], float]:
        
        for iteration in range(max_iterations):
            iteration_steps = []
            error_total = 0
            
            for i, input_values in enumerate(inputs):
                # Calcular la salida
                weighted_sum = sum(w * x for w, x in zip(self.weights, input_values)) + self.bias
                output = self.activation(weighted_sum)
                error = labels[i] - output
                error_total += abs(error)
                
                # Registrar el paso
                step_log = {
                    "input": input_values,
                    "weighted_sum": round(weighted_sum, 3),
                    "output": output,
                    "expected": labels[i],
                    "error": error
                }
                
                # Ajustar pesos y bias si hay error
                if error != 0:
                    old_weights = self.weights.copy()
                    old_bias = self.bias
                    
                    for j in range(len(self.weights)):
                        self.weights[j] += learning_rate * error * input_values[j]
                    self.bias += learning_rate * error
                    
                    step_log.update({
                        "weights_adjustment": [round(w - ow, 3) for w, ow in zip(self.weights, old_weights)],
                        "bias_adjustment": round(self.bias - old_bias, 3)
                    })
                
                iteration_steps.append(step_log)
            
            # Registrar la iteración
            self.logger.add_iteration(IterationLog(
                iteration=iteration + 1,
                weights=self.weights.copy(),
                bias=self.bias,
                total_error=error_total,
                steps=iteration_steps
            ))
            
            if error_total == 0:
                break
        
        # Guardar los logs
        self.logger.save()
        return self.weights, self.bias

def train_and_test_gate():
    # Datos de entrenamiento para la compuerta AND
    inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]
    labels_and = [0, 0, 0, 1]
    
    # Crear y entrenar el perceptrón
    perceptron = Perceptron(n_inputs=2)
    weights, bias = perceptron.train(inputs, labels_and)
    
    # Imprimir resumen
    print(perceptron.logger.get_summary())
    
    # Probar el perceptrón entrenado
    print("\nPruebas:")
    for input_values in inputs:
        weighted_sum = sum(w * x for w, x in zip(weights, input_values)) + bias
        output = perceptron.activation(weighted_sum)
        print(f"Entrada: {input_values}, Salida: {output}")

if __name__ == "__main__":
    train_and_test_gate()
```