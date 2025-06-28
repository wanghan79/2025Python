import random
import string
from typing import Any, Dict, Generator, List, Tuple, Union, Optional
from collections.abc import Mapping, Sequence


class DataSamplingError(Exception):
    """Custom exception for data sampling errors"""
    pass


def validate_config(config: Dict[str, Any], required_keys: List[str], config_type: str) -> None:
    """Validate configuration dictionary"""
    if not isinstance(config, dict):
        raise DataSamplingError(f"{config_type} config must be a dictionary")
    for key in required_keys:
        if key not in config:
            raise DataSamplingError(f"Missing required key '{key}' in {config_type} config")


def generate_primitive(data_type: str, config: Dict[str, Any]) -> Generator[Any, None, None]:
    """Generate primitive data types (int, float, str)"""
    try:
        if data_type == "int":
            validate_config(config, ["datarange"], "integer")
            low, high = config["datarange"]
            yield random.randint(low, high)
        elif data_type == "float":
            validate_config(config, ["datarange"], "float")
            low, high = config["datarange"]
            yield random.uniform(low, high)
        elif data_type == "str":
            validate_config(config, ["datarange", "len"], "string")
            chars = config["datarange"]
            length = config["len"]
            if not isinstance(chars, str):
                raise DataSamplingError("String datarange must be a string of characters")
            yield ''.join(random.choices(chars, k=length))
        else:
            raise DataSamplingError(f"Unsupported primitive type: {data_type}")
    except (TypeError, ValueError) as e:
        raise DataSamplingError(f"Invalid configuration for {data_type}: {str(e)}")


def generate_container(
        container_type: str,
        config: Dict[str, Any],
        size: Optional[int] = None
) -> Generator[Union[Tuple, List, Dict], None, None]:
    """Generate container types (tuple, list, dict)"""
    try:
        if container_type == "tuple":
            if not isinstance(config, Sequence):
                raise DataSamplingError("Tuple config must be a sequence")
            yield tuple(next(datasampling(**item)) for item in config)
        elif container_type == "list":
            if not isinstance(config, Sequence):
                raise DataSamplingError("List config must be a sequence")
            yield [next(datasampling(**item)) for item in config]
        elif container_type == "dict":
            if not isinstance(config, Mapping):
                raise DataSamplingError("Dict config must be a mapping")
            if size is not None:
                yield {f"key_{i}": next(datasampling(**config)) for i in range(size)}
            else:
                yield {key: next(datasampling(**value)) for key, value in config.items()}
        else:
            raise DataSamplingError(f"Unsupported container type: {container_type}")
    except (TypeError, ValueError) as e:
        raise DataSamplingError(f"Error generating {container_type}: {str(e)}")


def datasampling(**kwargs) -> Generator[Any, None, None]:
    """
    Main data sampling generator function

    Args:
        **kwargs: Configuration dictionary specifying data structure

    Yields:
        Generated data according to the configuration

    Raises:
        DataSamplingError: If configuration is invalid or generation fails
    """
    if not kwargs:
        raise DataSamplingError("Empty configuration provided")

    try:
        data_type, config = next(iter(kwargs.items()))

        # Handle size parameter for containers
        size = config.pop("size", None) if isinstance(config, dict) else None

        if data_type in ("int", "float", "str"):
            yield from generate_primitive(data_type, config)
        elif data_type in ("tuple", "list", "dict"):
            yield from generate_container(data_type, config, size)
        else:
            raise DataSamplingError(f"Unsupported data type: {data_type}")
    except StopIteration:
        raise DataSamplingError("Invalid configuration format")
    except Exception as e:
        raise DataSamplingError(f"Data generation failed: {str(e)}")


def batch_generator(config: Dict[str, Any], batch_size: int = 1) -> Generator[Any, None, None]:
    """Batch generator for efficient memory usage"""
    for _ in range(batch_size):
        try:
            yield next(datasampling(**config))
        except DataSamplingError as e:
            print(f"Skipping invalid sample: {str(e)}")
            continue


if __name__ == "__main__":
    # Example configuration with improved structure
    sample_config = {
        "dict": {
            "basic_info": {
                "tuple": [
                    {"str": {"datarange": string.ascii_uppercase, "len": 5}},
                    {"int": {"datarange": (0, 10)}}
                ]
            },
            "measurements": {
                "list": [
                    {"float": {"datarange": (0, 1.0)}},
                    {"int": {"datarange": (0, 100)}},
                    {"str": {"datarange": string.ascii_lowercase, "len": 8}}
                ],
                "size": 3  # Generate 3 measurements
            },
            "metadata": {
                "dict": {
                    "timestamp": {"int": {"datarange": (1609459200, 1640995200)}},
                    "location": {
                        "tuple": [
                            {"float": {"datarange": (-90.0, 90.0)}},
                            {"float": {"datarange": (-180.0, 180.0)}}
                        ]
                    }
                }
            }
        }
    }

    # Generate and print 5 samples
    print("Generating sample data...\n")
    try:
        for i, sample in enumerate(batch_generator(sample_config, 5), 1):
            print(f"Sample {i}:")
            print(sample)
            print("-" * 50)
    except DataSamplingError as e:
        print(f"Fatal error during generation: {str(e)}")