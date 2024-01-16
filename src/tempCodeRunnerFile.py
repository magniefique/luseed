
                file_name = os.path.basename(file.name)
            # Create a Lexer object and tokenize the file content
            code = Lexer(file_content, file_name)
            code.display_table("all")
            token_list = code.return_tokens()

        except FileNotFoundError:
            # Print error message if file is not found
            print(file_path)
            Error.FileError(file_path, Error.FileError.FILE_NOT_FOUND)

    elif file_path == "":
        # Call main if no input (Similar to python)
        main()
    
    else:
        # Print error message if the file ends with other file extension
        Error.FileError(file_path, Error.FileError.INVALID_FILE)
   
if __name__ == "__main__":
    main()