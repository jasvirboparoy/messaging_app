// The following code has been adapted from www.slackr.com.au
// Code was inspected and data was extracted to make this frontend
// component

import React from 'react';
import {
  Button,
  Dialog, DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Grid,
  MenuItem,
  Select
} from "@material-ui/core";
import axios from "axios";
import AuthContext from "../../AuthContext";

export class RemoveUserDialog extends React.Component {

  constructor() {
    super();
    this.state = {
      open: false,
      users: [],
      selectedUser: ""
    };

    this.handleClickOpen = this.handleClickOpen.bind(this);
    this.handleClose = this.handleClose.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleUserSelect = this.handleUserSelect.bind(this);
  }

  componentDidMount() {
    const { token } = this.props;
    axios
      .get('/users/all', {
        params: {
          token
        }
      })
      .then(({ data }) => {
        this.setState({
          users: data['users']
        });
      })
      .catch((err) => {});
  }

  handleClickOpen() {
    this.setState({
      open: true
    });
  }

  handleClose() {
    this.setState({
      open: false
    });
  }

  handleUserSelect(event) {
    const newUserId = parseInt(event.target.value,10);
    this.setState({
      selectedUser: newUserId
    });
  }

  handleSubmit(event) {
    event.preventDefault();

    if (!event.target[0].value) return;

    // Working
    const { token } = this.props;
    const u_id = parseInt(event.target[0].value,10);

    // Working
    console.log(token);
    console.log(u_id);

    // Working
    axios
      .delete(`/admin/user/remove`, { params: { token, u_id } })
      .then(response => {
        console.log(response);
        console.log(response.data);
      })
      .catch(err => {});
  }


  render() {
    const { open, users, selectedUser } = this.state;
    const { children } = this.props;
    return (
      <>
        <div onClick={this.handleClickOpen}>
          {children}
        </div>
        <Dialog
          open={open}
          onClose={this.handleClose}
          aria-labelledby="form-dialog-title"
        >
          <DialogTitle id="form-dialog-title">Remove User</DialogTitle>
          <form onSubmit={this.handleSubmit}>
            <DialogContent>
              <DialogContentText>
                Select a user below to remove from Slackr
              </DialogContentText>
              <Grid
                container
                spacing={2}
                direction="row"
                justify="center"
                alignItems="center"
              >
                <Grid item xs={12}>
                  <Select
                    style={{ width: "100%" }}
                    id="u_id"
                    onChange={this.handleUserSelect}
                    value={selectedUser}
                  >
                    {users.map(d => (
                      <MenuItem key={d.u_id} value={d.u_id}>
                        {d.name_first} {d.name_last}
                      </MenuItem>
                    ))}
                  </Select>
                </Grid>
              </Grid>
            </DialogContent>
            <DialogActions>
              <Button onClick={this.handleClose} color="primary">
                Cancel
              </Button>
              <Button onClick={this.handleClose} type="submit" color="primary">
                Remove
              </Button>
            </DialogActions>
          </form>
        </Dialog>
      </>
    );
  }
}
export default RemoveUserDialog;