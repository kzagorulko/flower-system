import React from 'react';
import classNames from 'classnames/bind';
import Card from '@material-ui/core/Card/Card';
import CardMedia from '@material-ui/core/CardMedia';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import CardActionArea from '@material-ui/core/CardActionArea';
import style from './style.less';

const cx = classNames.bind(style);

const UserCard = (params) => (
  <Card className={cx('Card')}>
    <CardActionArea className={cx('Container')} href={`/#/users/${params.user.id}`}>
      <CardMedia
        component="div"
        className={cx('Image')}
        image="https://yt3.ggpht.com/a/AATXAJwH1h8IT5kqsbQ5IeySczyEOvVa9CPB7SJDEGMoHQ=s900-c-k-c0x00ffffff-no-rj"
        title="user image"
      />
      <CardContent component="div">
        <Typography component="div" variant="subtitle1">
          {params.user.displayName}
        </Typography>
        <Typography component="div" variant="subtitle2">
          {params.user.role}
        </Typography>
      </CardContent>
    </CardActionArea>
  </Card>
);

export default UserCard;
