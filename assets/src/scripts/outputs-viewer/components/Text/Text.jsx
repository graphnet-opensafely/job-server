import PropTypes from "prop-types";
import React from "react";
import classes from "./Text.module.scss";

function Text({ data }) {
  return <pre className={classes.txt}>{data}</pre>;
}

Text.propTypes = {
  data: PropTypes.string.isRequired,
};

export default Text;