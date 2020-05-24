import { red } from '@material-ui/core/colors';
import { createMuiTheme } from '@material-ui/core/styles';

// A custom theme for this app
const theme = createMuiTheme({
  palette: {
    primary: {
      main: '#4299E1',
    },
    secondary: {
      main: '#4C51BF',
    },
    error: {
      main: red.A400,
    },
    background: {
      default: '#F7FAFC',
    },
  },
});

export default theme;