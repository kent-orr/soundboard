# Soundboard

A Raspberry Pi Zero W2-based soundboard application.

---

## Button Layout

The soundboard has 10 physical buttons arranged in a **5 × 2 grid** — two of each color. Each label shows the button color and row number:

```
  ┌──────┬──────┬──────┬──────┬──────┐
  │  R1  │  G1  │  B1  │  Y1  │  W1  │  ← Row 1
  ├──────┼──────┼──────┼──────┼──────┤
  │  R2  │  G2  │  B2  │  Y2  │  W2  │  ← Row 2
  └──────┴──────┴──────┴──────┴──────┘
```

| Label | Color  | BCM GPIO | Board Pin |
|-------|--------|----------|-----------|
| R1    | Red    | GPIO17   | 11        |
| G1    | Green  | GPIO27   | 13        |
| B1    | Blue   | GPIO22   | 15        |
| Y1    | Yellow | GPIO23   | 16        |
| W1    | White  | GPIO24   | 18        |
| R2    | Red    | GPIO25   | 22        |
| G2    | Green  | GPIO5    | 29        |
| B2    | Blue   | GPIO6    | 31        |
| Y2    | Yellow | GPIO16   | 36        |
| W2    | White  | GPIO26   | 37        |

> Each button connects between its GPIO pin and GND. GPIO pins use internal pull-up resistors — pressing a button pulls the line LOW.

### GPIO Header with Button Assignments

Button labels shown as `(label)` on their assigned pin:

```
                       3V3  [ 1] [ 2]  5V
             GPIO2 (SDA1)  [ 3] [ 4]  5V
             GPIO3 (SCL1)  [ 5] [ 6]  GND
                   GPIO4  [ 7] [ 8]  GPIO14 (TXD0)
                     GND  [ 9] [10]  GPIO15 (RXD0)
             GPIO17 (R1)  [11] [12]  GPIO18 (PCM_CLK)
             GPIO27 (G1)  [13] [14]  GND
             GPIO22 (B1)  [15] [16]  GPIO23 (Y1)
                     3V3  [17] [18]  GPIO24 (W1)
      GPIO10 (SPI0_MOSI)  [19] [20]  GND
       GPIO9 (SPI0_MISO)  [21] [22]  GPIO25 (R2)
      GPIO11 (SPI0_SCLK)  [23] [24]  GPIO8  (SPI0_CE0_N)
                     GND  [25] [26]  GPIO7  (SPI0_CE1_N)
       GPIO0 (ID_SD/I2C)  [27] [28]  GPIO1  (ID_SC/I2C)
              GPIO5 (G2)  [29] [30]  GND
              GPIO6 (B2)  [31] [32]  GPIO12 (PWM0)
          GPIO13 (PWM1)   [33] [34]  GND
   GPIO19 (PCM_FS/SPI1)   [35] [36]  GPIO16 (Y2)
             GPIO26 (W2)  [37] [38]  GPIO20 (PCM_DIN/SPI1)
                     GND  [39] [40]  GPIO21 (PCM_DOUT/SPI1)
```

---

## Raspberry Pi Zero W2 GPIO Pinout

The Pi Zero W2 has a 40-pin GPIO header. Pins are numbered in two ways:
- **Board**: physical pin position (1–40)
- **BCM**: Broadcom GPIO number (used in software)

```
                       3V3  [ 1] [ 2]  5V
             GPIO2 (SDA1)  [ 3] [ 4]  5V
             GPIO3 (SCL1)  [ 5] [ 6]  GND
                   GPIO4  [ 7] [ 8]  GPIO14 (TXD0)
                     GND  [ 9] [10]  GPIO15 (RXD0)
                  GPIO17  [11] [12]  GPIO18 (PCM_CLK)
                  GPIO27  [13] [14]  GND
                  GPIO22  [15] [16]  GPIO23
                     3V3  [17] [18]  GPIO24
      GPIO10 (SPI0_MOSI)  [19] [20]  GND
       GPIO9 (SPI0_MISO)  [21] [22]  GPIO25
      GPIO11 (SPI0_SCLK)  [23] [24]  GPIO8  (SPI0_CE0_N)
                     GND  [25] [26]  GPIO7  (SPI0_CE1_N)
       GPIO0 (ID_SD/I2C)  [27] [28]  GPIO1  (ID_SC/I2C)
                   GPIO5  [29] [30]  GND
                   GPIO6  [31] [32]  GPIO12 (PWM0)
          GPIO13 (PWM1)   [33] [34]  GND
   GPIO19 (PCM_FS/SPI1)   [35] [36]  GPIO16 (SPI1_CE2_N)
                  GPIO26  [37] [38]  GPIO20 (PCM_DIN/SPI1)
                     GND  [39] [40]  GPIO21 (PCM_DOUT/SPI1)
```

### Pin Reference Table

| Board Pin | BCM GPIO | Function              | Notes                        |
|-----------|----------|-----------------------|------------------------------|
| 1         | —        | 3.3V Power            |                              |
| 2         | —        | 5V Power              |                              |
| 3         | GPIO2    | SDA1 (I2C)            | Has 1.8kΩ pull-up            |
| 4         | —        | 5V Power              |                              |
| 5         | GPIO3    | SCL1 (I2C)            | Has 1.8kΩ pull-up            |
| 6         | —        | Ground                |                              |
| 7         | GPIO4    | GPCLK0                |                              |
| 8         | GPIO14   | TXD0 (UART)           |                              |
| 9         | —        | Ground                |                              |
| 10        | GPIO15   | RXD0 (UART)           |                              |
| 11        | GPIO17   | —                     |                              |
| 12        | GPIO18   | PCM_CLK / PWM0        |                              |
| 13        | GPIO27   | —                     |                              |
| 14        | —        | Ground                |                              |
| 15        | GPIO22   | —                     |                              |
| 16        | GPIO23   | —                     |                              |
| 17        | —        | 3.3V Power            |                              |
| 18        | GPIO24   | —                     |                              |
| 19        | GPIO10   | SPI0_MOSI             |                              |
| 20        | —        | Ground                |                              |
| 21        | GPIO9    | SPI0_MISO             |                              |
| 22        | GPIO25   | —                     |                              |
| 23        | GPIO11   | SPI0_SCLK             |                              |
| 24        | GPIO8    | SPI0_CE0_N (CS0)      |                              |
| 25        | —        | Ground                |                              |
| 26        | GPIO7    | SPI0_CE1_N (CS1)      |                              |
| 27        | GPIO0    | ID_SD (I2C EEPROM)    | Reserved for HAT ID          |
| 28        | GPIO1    | ID_SC (I2C EEPROM)    | Reserved for HAT ID          |
| 29        | GPIO5    | —                     |                              |
| 30        | —        | Ground                |                              |
| 31        | GPIO6    | —                     |                              |
| 32        | GPIO12   | PWM0                  |                              |
| 33        | GPIO13   | PWM1                  |                              |
| 34        | —        | Ground                |                              |
| 35        | GPIO19   | PCM_FS / SPI1_MISO    |                              |
| 36        | GPIO16   | SPI1_CE2_N            |                              |
| 37        | GPIO26   | —                     |                              |
| 38        | GPIO20   | PCM_DIN / SPI1_MOSI   |                              |
| 39        | —        | Ground                |                              |
| 40        | GPIO21   | PCM_DOUT / SPI1_SCLK  |                              |

### Power Rails

| Pin(s)       | Voltage | Max Current |
|--------------|---------|-------------|
| 2, 4         | 5V      | ~1A (shared with board) |
| 1, 17        | 3.3V    | 300mA total |
| 6, 9, 14, 20, 25, 30, 34, 39 | GND | — |

### Key Interfaces

| Interface | Pins (BCM)             | Board Pins          |
|-----------|------------------------|---------------------|
| I2C0      | GPIO0 (SDA), GPIO1 (SCL) | 27, 28            |
| I2C1      | GPIO2 (SDA), GPIO3 (SCL) | 3, 5              |
| SPI0      | GPIO10 (MOSI), GPIO9 (MISO), GPIO11 (SCLK), GPIO8 (CE0), GPIO7 (CE1) | 19, 21, 23, 24, 26 |
| SPI1      | GPIO20 (MOSI), GPIO19 (MISO), GPIO21 (SCLK), GPIO16 (CE2) | 38, 35, 40, 36 |
| UART0     | GPIO14 (TX), GPIO15 (RX) | 8, 10             |
| PWM       | GPIO12 (PWM0), GPIO13 (PWM1), GPIO18 (PWM0), GPIO19 (PWM1) | 32, 33, 12, 35 |
| PCM/I2S   | GPIO18 (CLK), GPIO19 (FS), GPIO20 (DIN), GPIO21 (DOUT) | 12, 35, 38, 40 |

> **Note:** GPIO pins operate at 3.3V logic. Do **not** connect 5V signals directly — use a level shifter.
