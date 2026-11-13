
def practice_3_complete_pattern():
    """
    Practice with try-except-else-finally
    """

    print("\n" + "=" * 50)
    print("EXERCISE 3: Complete Exception Pattern")
    print("=" * 50)

    
    def process_file(filename):
        """
        Read file, process content, ensure file is closed.
        Return processed content or None.
        """
        file = None

        try:
            file = open(filename, "r")

        except FileNotFoundError:
            print(f"File '{filename}' was not found.")
            return None

        except PermissionError:
            print(f"Permission denied for '{filename}'.")
            return None

        else:
            content = file.read()
            processed = content.upper().split()
            return processed

        finally:
            if file is not None:
                file.close()
                print("File closed.")

    
    test_files = ["exists.txt", "missing.txt", "/root/file"]

    for filename in test_files:
        result = process_file(filename)
        print(f"Processing '{filename}': {result}")

    
    class ResourceManager:

        def __init__(self, name):
            self.name = name
            self.resource = None

        def acquire(self):
            """Acquire resource - might fail."""
            if self.resource is not None:
                raise RuntimeError("Resource is already acquired.")

            self.resource = True
            print(f"{self.name} resource acquired.")

        def release(self):
            """Release resource - must always happen."""
            if self.resource is not None:
                self.resource = None
                print(f"{self.name} resource released.")

        def use(self):
            """Use resource - only if acquired."""
            if self.resource is None:
                raise RuntimeError("Resource must be acquired first.")

            print(f"Using {self.name} resource.")


    rm = ResourceManager("Database")

    try:
        rm.acquire()

    except RuntimeError as e:
        print(f"Error: {e}")

    else:
        rm.use()

    finally:
        rm.release()


def practice_2_custom_exceptions():
    """
    Practice creating and using custom exceptions
    """

    print("\n" + "=" * 50)
    print("EXERCISE 5: Custom Exceptions")
    print("=" * 50)

   
    class GameError(Exception):
        """Base class for game exceptions."""
        pass

    class InvalidMoveError(GameError):
        """Invalid game move."""

        def __init__(self, position, reason):
            self.position = position
            self.reason = reason
            super().__init__(
                f"Invalid position {position}: {reason}"
            )

    class GameOverError(GameError):
        """Game has ended."""

        def __init__(self, winner):
            self.winner = winner
            super().__init__(f"Game is over. Winner: {winner}")

    
    class TicTacToe:

        def __init__(self):
            self.board = [[' ' for _ in range(3)] for _ in range(3)]
            self.current_player = 'X'
            self.game_over = False

        def make_move(self, row, col):

            if self.game_over:
                raise GameOverError("No more moves allowed")

            if not (0 <= row < 3 and 0 <= col < 3):
                raise InvalidMoveError(
                    (row, col), "Position is out of bounds"
                )

            if self.board[row][col] != ' ':
                raise InvalidMoveError(
                    (row, col), "Position is already taken"
                )

            self.board[row][col] = self.current_player

            self.current_player = (
                'O' if self.current_player == 'X' else 'X'
            )

    
    game = TicTacToe()

    test_moves = [
        (0, 0),
        (0, 0),
        (5, 5)
    ]

    for row, col in test_moves:
        try:
            game.make_move(row, col)
            print(f"Move ({row}, {col}) successful")

        except InvalidMoveError as e:
            print(f"Invalid move: {e}")

        except GameOverError as e:
            print(f"Game over: {e}")


practice_2_custom_exceptions()


def practice_3_complete_system():
    """
    Build a complete error handling system
    """

    print("\n" + "=" * 50)
    print("EXERCISE 6: Complete Error Handler")
    print("=" * 50)

    import os

    
    class FileProcessor:

        def __init__(self):
            self.processed_files = []
            self.failed_files = []

        def process_file(self, filename):
            """
            Process a single file with complete error handling.
            """
            file = None

            try:
                file = open(filename, "r")
                content = file.read()

            except FileNotFoundError as e:
                print(f"File not found: {filename}")
                self.failed_files.append(filename)
                return False

            except PermissionError as e:
                print(f"Permission denied: {filename}")
                self.failed_files.append(filename)
                return False

            except Exception as e:
                print(f"Unexpected error with {filename}: {e}")
                self.failed_files.append(filename)
                return False

            else:
                print(f"Successfully processed: {filename}")
                self.processed_files.append(filename)
                return True

            finally:
                if file is not None:
                    file.close()
                    print(f"Closed: {filename}")

        def process_directory(self, directory):
            """
            Process all files in directory, collecting errors.
            """
            try:
                for filename in os.listdir(directory):
                    filepath = os.path.join(directory, filename)

                    if os.path.isfile(filepath):
                        self.process_file(filepath)

            except FileNotFoundError:
                print(f"Directory not found: {directory}")

            except PermissionError:
                print(f"Permission denied: {directory}")

        def get_report(self):
            """
            Get processing report.
            """
            return {
                "successful_count": len(self.processed_files),
                "failed_count": len(self.failed_files),
                "processed_files": self.processed_files,
                "failed_files": self.failed_files
            }

  
    processor = FileProcessor()

    test_files = [
        "valid.txt",
        "missing.txt",
        "/root/restricted.txt"
    ]

    for filename in test_files:
        processor.process_file(filename)

    report = processor.get_report()
    print(f"Report: {report}")



practice_3_complete_system()


