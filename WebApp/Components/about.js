
// Components/about.js
module.exports = `
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About Us</title>
    <style>
        /* Reset CSS */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f4;
            color: #333;
            line-height: 1.6;
        }

        .container {
            width: 80%;
            margin: auto;
            overflow: hidden;
        }

        header {
            background: #333;
            color: #fff;
            padding: 20px 0;
        }

        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 24px;
            text-decoration: none;
            color: #fff;
        }

        .nav-links {
            list-style: none;
            display: flex;
        }

        .nav-links li {
            margin-right: 20px;
        }

        .nav-links li a {
            text-decoration: none;
            color: #fff;
            transition: color 0.3s ease;
        }

        .nav-links li a:hover {
            color: #ccc;
        }

        #about {
            background-color: #fff;
            padding: 50px;
            border-radius: 5px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }

        #about h2 {
            font-size: 36px;
            margin-bottom: 20px;
        }

        #about p {
            font-size: 16px;
            margin-bottom: 15px;
        }

        footer {
            background: #333;
            color: #fff;
            padding: 20px 0;
            text-align: center;
        }
    </style>
</head>

<body>
    <header>
        <nav class="navbar">
            <div class="container">
                <a href="#" class="logo">My Website</a>
                <ul class="nav-links">
                    <li><a href="/">Home</a></li>
                    <li><a href="#">About</a></li>
                    <li><a href="#">Services</a></li>
                    <li><a href="#">Contact</a></li>
                </ul>
            </div>
        </nav>
    </header>

    <div class="container">
        <section id="about">
            <h2>About Us</h2>
            <p>Welcome to our website! We are a team of passionate individuals dedicated to providing high-quality services.</p>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla venenatis sapien id libero volutpat, vitae cursus lectus posuere. Nullam in urna ac felis tincidunt eleifend et at libero. Suspendisse potenti. Proin eget risus a libero luctus suscipit. Phasellus volutpat, justo vel cursus condimentum, eros orci sodales ante, in semper neque odio eget dolor. Morbi viverra urna velit, eget ultricies magna blandit ut. Vestibulum scelerisque quam eget lacus volutpat, vel suscipit lacus placerat.</p>
            <p>Curabitur non ligula ut ipsum placerat fermentum. Nullam consequat nulla id aliquam semper. Aliquam erat volutpat. Integer eget ligula ut nisl commodo fermentum sed in lectus. Mauris faucibus, neque a vehicula tincidunt, magna turpis finibus risus, at vestibulum lacus mi nec enim. Fusce feugiat, eros ac imperdiet aliquam, nisi elit suscipit lorem, in vulputate nisi nisl vitae justo. Vivamus laoreet ultrices sapien, nec facilisis tortor lobortis at.</p>
            <p>Donec id efficitur tortor. Nulla facilisi. Integer id erat vitae libero luctus mattis. Donec lacinia nisl eu libero rutrum, vel fermentum sem tempus. Duis vel magna id est fermentum tincidunt sed id orci. Ut venenatis nec dui ac sollicitudin. Ut fringilla, ligula eget congue elementum, libero est interdum diam, sit amet egestas magna velit sit amet odio. Nullam rhoncus sem eget ex facilisis, nec tempor sem vestibulum.</p>
        </section>
    </div>

    <footer>
        <div class="container">
            <p>&copy; 2024 My Website. All rights reserved.</p>
        </div>
    </footer>
</body>

</html>


`;