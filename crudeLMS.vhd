--Crudest possible functioning LMS
--8 taps only~

library ieee;
use ieee.numeric_std.all;
use ieee.std_logic_1164.all;



entity crudeLMS is
	generic (g_width 	: integer:=12;
				g_mu		: integer:=5);
	port (	i_clk 	: in std_logic;
				i_reset	: in std_logic;
				i_refere	: in signed (g_width-1 downto 0);
				i_contam : in signed (g_width-1 downto 0);
				o_output	: out signed (g_width-1 downto 0));
end crudeLMS;


architecture arch of crudeLMS is
	
	type t_taps is array (0 to 7) of unsigned (g_width-1 downto 0);
	type t_past is array (0 to 7+2) of unsigned (g_width-1 downto 0);
	signal a_taps 	: t_taps; 
	signal a_result: t_taps;
	signal a_past 	: t_taps;
	
	signal r_error : signed(g_width-1 downto 0);
	constant c_delay : integer:=2;
	
begin
	--This means that there will be one stage for the multiplications
	--Smallest number is for the current input

	
	o_output <= r_error;

	MAIN: process(i_clk, i_reset, i_refere, i_contam)
		variable v_sum : signed(g_width+3-1 downto 0);
		variable v_errorDataProduct : signed(g_width-1 downto 0);
	begin
		--First stage
		for R in 1 to 7 loop
			a_result(R) <= a_taps(R) * a_past(R);
		end loop;
		a_result(0) <= a_taps(0) * i_refere;
		
		--Second stage
		for R in 0 to 7 loop
			r_sum := r_sum + resize(a_result(R), g_width+3);
		end loop;	
		r_error <= i_contam - v_sum(g_width+3-1 downto 3);
	
		--Third!
		for T in 0 to 7 loop
			v_errorDataProduct := r_error * a_past(T+2);
			a_taps(T) <= a_taps(T) + shift_left(v_errorDataProduct, mu);
		end loop;
		
		--Shift register of past values
		for T in 1 to 7+2 loop
			a_past(T) <= a_past(T-1);
		end loop;
		a_taps(0) <= i_refere;
		
	end process;

end arch;