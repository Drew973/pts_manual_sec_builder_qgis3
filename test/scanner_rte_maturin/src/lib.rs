// rustimport:pyo3
use pyo3::prelude::*;
//use anyhow::Result;
use serde::{Serialize, Deserialize};

/// A Python module implemented in Rust.
#[pymodule]
mod greece_rte {
    use pyo3::prelude::*;



	#[pyclass]
	#[derive(Deserialize)]
	enum Direction {
		NB,
		EB,
		WB,
		SB,
		CW,
		AC
	}
	
	#[pymethods]
	impl Direction
	{
		
		#[staticmethod]
		fn from_str(s: &str) -> PyResult<Direction>
			{
				(Err("an error"))
			}
		
		
	}




	#[pyclass]
	struct R2_1
	{
		section_label: String,
		direction: Direction,
		lane_name: String,
		start_chainage: f32,
		end_chainage: f32,
		start_reference_label: String,
		start_x: f32,
		start_y: f32
		
	}

	#[pymethods]
	impl R2_1
	{
		#[staticmethod]
		fn from_line(line: &str) -> PyResult<R2_1>
		{
			if line.len() < 116 {
				(Err("R2_1 line < 116 charactors long"))
			}
			
		
			
			Ok(
				R2_1{section_label: line[0..30].to_string(),
					direction: Direction::from_str(&line[30..32])?,
					lane_name: line[32..52].to_string(),
					start_chainage: line[53..63].parse()?,
					end_chainage: 0.0,
					start_reference_label: line[74..94].to_string(),
					start_x: 0.0,
					start_y: 0.0
				}
			)
			
			
		}
		
		
	}




    /// Formats the sum of two numbers as string.
    #[pyfunction]
    fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
        Ok((a + b).to_string())
    }
}
