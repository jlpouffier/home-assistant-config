#include "esphome.h"
#include <bitset>

class DeskHeightSensor : public Component, public UARTDevice, public Sensor
{
public:
  DeskHeightSensor(UARTComponent *parent) : UARTDevice(parent) {}

  float get_setup_priority() const override { return esphome::setup_priority::DATA; }

  Sensor *height_sensor = new Sensor();

  float height = -1;
  float lastPublishedHeight = -1;

  unsigned long history[5];

  void setup() override
  {
    // nothing to do here
  }

  void loop() override
  {
    while (available() > 0)
    {
      byte incomingByte = read();

      history[4] = history[3];
      history[3] = history[2];
      history[2] = history[1];
      history[1] = history[0];
      history[0] = incomingByte;

      if (history[4] == 0x98 && history[3] == 0x98)
      {
        height = incomingByte;
        if (lastPublishedHeight != height)
        {
          height_sensor->publish_state(height);
          lastPublishedHeight = height;
        }
      }
    }
  }
};