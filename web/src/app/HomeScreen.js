import * as React from "react";
import Button from '@material-ui/core/Button';
import TextField from "@material-ui/core/TextField";
import GridList from "@material-ui/core/GridList";
import GridListTile from "@material-ui/core/GridListTile";
import ListSubheader from "@material-ui/core/ListSubheader";
import {withStyles, withTheme} from "@material-ui/core/styles";
import GridListTileBar from "@material-ui/core/GridListTileBar";
import axios from "axios";

class HomeScreen extends React.Component {
  constructor() {
    super();
    this.state = {
      searchText: "",
      searchResults: []
    };
    this.handleChange = this.handleChange.bind(this)
    this.searchSimilarImages = this.searchSimilarImages.bind(this)
  }

  componentDidMount() {

  }

  searchSimilarImages() {
    const imageId = this.state.searchText;
    const self = this;
    axios.post('/api/v1/query', {
      id: imageId
    })
    .then(function (response) {
      // debugger;
      self.setState({
        searchResults: response.data
      });
      console.log(response)
    })
    .catch(function (error) {
      console.log(error);
    });
  }

  handleChange(event) {
    this.setState({searchText: event.target.value});
  }

  getImagePath(imageName) {
    const rootPath = "http://localhost:8080/myntradataset/images/"
    return rootPath + imageName;
  }

  render() {
    const classes = this.props;
    // debugger;
    const {searchResults} = this.state;
    const {searchText} = this.state;

    return (
        <div>
          <div>
            <TextField label="Search" variant="outlined" name="searchBox"
                       id="search-field" value={searchText}
                       onChange={this.handleChange}/>
            <Button variant="contained" color="primary"
                    onClick={this.searchSimilarImages}>Search</Button>
          </div>
          <div>
            <h3>Searched Image</h3>
            <img src={this.getImagePath(searchText +".jpg")}
                 alt={searchText}/>
          </div>
          <div>
            <GridList cellHeight={180} className={classes.gridList}>
              <GridListTile key="Subheader" cols={2} style={{height: 'auto'}}>
                <ListSubheader component="div">Search results</ListSubheader>
              </GridListTile>
              {searchResults.map((tile) => (
                  <GridListTile key={tile.content} className={classes.gridListTile}>
                    <img src={this.getImagePath(tile.content)}
                         alt={tile.title} className={classes.displayImage} style={{height:100,width:100}}/>
                    <GridListTileBar
                        title={tile.title}
                        subtitle={<span>by: {tile.content_id}</span>}
                    />
                  </GridListTile>
              ))}
            </GridList>

          </div>
        </div>
    )
  }
}

const styles = (theme) => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    overflow: 'hidden',
    // backgroundColor: theme.palette.background.paper,
  },
  gridList: {
    width: 500,
    height: 450,
  },
  gridListTile:{
    height:250,
    width:250,
  },
  displayImage :{
    height:100,
    width:100,
  },
  icon: {
    color: 'rgba(255, 255, 255, 0.54)',
  },
  queryImage: {
    maxHeight: 250
  }
});

export default withStyles(styles)(HomeScreen)
