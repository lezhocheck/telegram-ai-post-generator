import { Outlet } from 'react-router-dom'
import { Helmet } from 'react-helmet';
import Header from '../main/header/Header';
import Footer from '../main/footer/Footer';
import favicon from '../../static/favicon.png';

const Layout = () =>
{
    return (
        <div className="App">
            <Helmet>
                <meta charSet="utf-8" />
                <title>ImGen</title>
                <link rel="icon" href={favicon} />
                <style>{"body { background-color: #212529; }"}</style>
            </Helmet>
            <Header />
            <Outlet />
            <Footer />
        </div>
    );
}

export default Layout;