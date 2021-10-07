import { Card, CardContent, Typography, ListItemText, ListItem, List, CardActions, Collapse, Button, IconButton } from '@material-ui/core'
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import { styled } from '@material-ui/core/styles';
import React from 'react'
import './InfoBox.css';

const style = {
  height: '100%',
  width: '100%',
  maxWidth: 360,
  bgcolor: 'background.paper',
};

const ExpandMore = styled((props) => {
  const { expand, ...other } = props;
  return <IconButton {...other} />;
})(({ theme, expand }) => ({
  transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
  marginLeft: 'auto',
  transition: theme.transitions.create('transform', {
    duration: theme.transitions.duration.shortest,
  }),
}));


function InfoBox({title,value,active,percap,percent, onClick,date}) {
    const [expanded, setExpanded] = React.useState(false);

    const handleExpandClick = () => {
        setExpanded(!expanded);
    };
    if(percent === '100 %'){
    return (
        <Card onClick={onClick} className={`infobox ${active && 'infobox--selected'}`}>
                <CardContent>
                    <Typography color="textSecondary" varient = "overline"className="infobox__title">{title}</Typography>
                    <h1 className="infobox_value">{value}</h1>
                    <h2 className="infobox_value">{percap}</h2>
                    <h2 className="infobox_value">{percent}</h2>
            <Typography style={{marginTop:10}}color="textSecondary" varient="subtitle2">{date}</Typography>
                </CardContent>
        </Card>
        )
    }
    else{
    return (
        <Card onClick={onClick} className={`infobox ${active && 'infobox--selected'}`}>
            <CardContent>
                <Typography color="textSecondary" varient = "overline"className="infobox__title">{title}</Typography>
                <h1 className="infobox_value">{value}</h1>
                <h2 className="infobox_value">{percap}</h2>
                <h2 className="infobox_value">{percent}</h2>
        <Typography style={{marginTop:10}}color="textSecondary" varient="subtitle2">{date}</Typography>
            </CardContent>
            <CardActions>
                <ExpandMore
                    expand={expanded}
                    onClick={handleExpandClick}
                    aria-expanded={expanded}
                    aria-label="show more"
                    >
                <ExpandMoreIcon />
                </ExpandMore>

            </CardActions>
            <Collapse in={expanded} timeout="auto" unmountOnExit>
            <List sx={style} component="nav" aria-label="mailbox folders">
                <ListItem button>
                    <ListItemText primary="Paper" />
                </ListItem>
                <ListItem button>
                    <ListItemText primary="Furniture" />
                </ListItem>
            </List>
            </Collapse>

        </Card>
    )
}}

export default InfoBox