import React from 'react';
import { Chip } from '@material-ui/core';
import classNames from 'classnames/bind';

import style from './style.less';

const cx = classNames.bind(style);

const QuickFilter = ({ label }) => (
  <Chip component="span" className={cx('Chip')} label={<span className={cx('Label')}>{label}</span>} />
);

export default QuickFilter;
