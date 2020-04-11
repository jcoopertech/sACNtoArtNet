## Properties of Art-Net and sACN packets

| Art-Net      | sACN          | Comment  |
| :----------: |:-------------:| :-----:|
|  OpCode      |   Vector      | Defines the type of package that is beeing sent |
|  Sequence    |  Sequence     | Art-Net: 0 = disabled  |
| Physical     |      -        | Defines from which physical port the package was sent  |
|Sub Uni       |       Universe| Art-Net: Has Sub Universe and Net |
|Net           |...            |sACN: Has Universe only|
|  -           | Start Code    | Art-Net: is defined by OPCode|
|  -           | Options       | Art-Net: is defined by other packets|
|  -           | CID           | sACN: UUID of sender |
|  -           | Priority      | |
|  -           | Source Name   | Art-Net: definde by other packets |
| DMX data     | DMX data      | |
