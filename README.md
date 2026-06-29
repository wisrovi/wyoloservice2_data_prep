# wyoloservice2_data_prep

Librería de preprocesamiento, validación de datasets YOLO y notificaciones de Slack para NeuralForgeAI.

## Instalación

```bash
pip install -e .
```

## Uso de Validación

Puedes usarlo programáticamente:
```python
from wyolo_data_prep import check_yolo_dataset

resultado = check_yolo_dataset("/mnt/datos/yolo/dataset.yaml")
print(resultado)
```

O desde la línea de comandos:
```bash
wyolo-validate --yaml /mnt/datos/yolo/dataset.yaml
```

## Uso del Notificador de Slack

Configura la variable de entorno `SLACK_WEBHOOK_URL` y luego:
```python
from wyolo_data_prep import SlackNotifier

notifier = SlackNotifier()
notifier.send_alert("Entrenamiento Terminado", "El estudio 123 ha finalizado con 98% de precisión", level="success")
```