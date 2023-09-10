import styles from './CoverSection.module.scss';
import {useTranslation} from 'react-i18next';
import { SiPowershell } from 'react-icons/si';

const CoverSection = () => {
    const {t} = useTranslation();

    return (
        <SiPowershell size={400} color='#FFFFFF'/>
    );    
}

export default CoverSection;