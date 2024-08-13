location_map = {'N': 1,
                'S': -1,
                'E': 1,
                'W': -1}
zurich_map = {'A': 1,
              'B': 2,
              'C': 3,
              'D': 4,
              'E': 5,
              'F': 6,
              'H': 7,
              'X': 0}
penumbra_map = {'X': 1,
                'R': 2,
                'S': 3,
                'A': 4,
                'H': 5,
                'K': 6,
                'O': 0}
compactness_map = {'X': 1,
                   'O': 2,
                   'I': 3,
                   'C': 4}
xray_class_map = {'A': 1e-8,
                  'B': 1e-7,
                  'C': 1e-6,
                  'M': 1e-5,
                  'X': 1e-4}

inverse_mapping = lambda _map: {_v: _k for _k, _v in _map.items()}