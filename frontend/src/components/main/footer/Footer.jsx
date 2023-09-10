import React from 'react';
import { TbRobot } from 'react-icons/tb';
import { AiOutlineHome, AiOutlineMail, AiOutlinePhone } from 'react-icons/ai';
import { MDBFooter, MDBContainer, MDBRow, MDBCol } from 'mdb-react-ui-kit';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';

const Footer = () =>
{
    const { t } = useTranslation();

    return (
        <MDBFooter bgColor="dark" className="text-center text-lg-start text-muted">
            <section>
                <MDBContainer className="text-center text-md-start mt-5">
                    <MDBRow className="mt-3">
                        <MDBCol md="3" lg="4" xl="3" className="mx-auto mb-4">
                            <h6 className="text-uppercase fw-bold mb-4">
                                <TbRobot size={30} /> ImGen
                            </h6>
                            <p>
                                {t("footer_desc")}
                            </p>
                        </MDBCol>
                        <MDBCol md="4" lg="3" xl="3" className="mx-auto mb-md-0 mb-4">
                            <h6 className="text-uppercase fw-bold mb-4">{t("contacts")}</h6>
                            <p><AiOutlineHome size={20} /> {t("address")}</p>
                            <p><AiOutlineMail size={20} /> info@imgen.com</p>
                            <p><AiOutlinePhone size={20} /> +380 (68) 000-00-00</p>
                            <p><AiOutlinePhone size={20} /> +380 (99) 111-11-11</p>
                        </MDBCol>
                    </MDBRow>
                </MDBContainer>
            </section>
            <div className="text-center p-4" style={{ backgroundColor: "rgba(0, 0, 0, 0.05)" }}>
                <span>© 2023 Copyright </span>
                <Link to='/' className='text-secondary' style={{ textDecoration: 'none' }}>imgen.com</Link>
            </div>
        </MDBFooter>
    );
}

export default Footer;