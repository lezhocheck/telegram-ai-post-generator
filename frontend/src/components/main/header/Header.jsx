import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import { TbRobot } from 'react-icons/tb';
import { FaUserAlt, FaLanguage } from 'react-icons/fa';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import styles from './Header.module.scss';
import useAuth from '../../../hooks/useAuth';

const Header = () =>
{
    const { t, i18n } = useTranslation();
    const { auth } = useAuth();

    return (
        <Navbar sticky='top' bg='bg-dark' variant='dark'>
            <Container>
                <Navbar.Brand>
                    <Link to='/' style={{ textDecoration: 'none', color: 'white' }}>
                        <TbRobot size={40} /> ImGen
                    </Link>
                </Navbar.Brand>
                <Nav className='ml-auto'>
                    <Nav.Item className={styles.profile}>
                        <NavDropdown title={
                            <span><FaLanguage size={30} /> {t('main.lang')}</span>
                        } onSelect={i18n.changeLanguage}>
                            <NavDropdown.Item eventKey='en'>English</NavDropdown.Item>
                            <NavDropdown.Item eventKey='ua'>Українська</NavDropdown.Item>
                        </NavDropdown>
                    </Nav.Item>
                    <Nav.Item className={styles.profile}>
                        <Link to='/profile' style={{ textDecoration: 'none', color: 'white' }}>
                            <FaUserAlt size={18} />
                            {
                                auth?.email ? `${auth.email}` : ` ${t('main.profile')}`
                            }
                        </Link>
                    </Nav.Item>
                </Nav>
            </Container>
        </Navbar>
    );
}

export default Header;