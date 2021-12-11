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
				o_debug : out signed (g_width-1 downto 0);
				o_output	: out signed (g_width-1 downto 0));
end crudeLMS;


architecture arch of crudeLMS is
	
	constant c_delay : integer:=2;
	type t_taps is array (0 to 7) of signed (g_width-1 downto 0);
	type t_result is array (0 to 7) of signed (g_width*2-1 downto 0);
	type t_past is array (0 to 7+c_delay) of signed (g_width-1 downto 0);
	
	signal a_taps 	: t_taps; 
	signal a_result: t_result;
	signal a_past 	: t_past;
	
	signal r_error : signed(g_width-1 downto 0);
	
begin
	--This means that there will be one stage for the multiplications
	--Smallest number is for the current input

	
	o_output <= r_error;
	o_debug <= a_result(0)(g_width-1 downto 0);
	
	MAIN: process(i_clk, i_reset, i_refere, i_contam)
		variable v_sum : signed(2*g_width+3-1 downto 0) := (others=> '0');
		variable v_errorDataProduct : signed(2*g_width-1 downto 0);
	begin
		
		if (i_reset = '1') then
			for R in a_taps'range loop
				a_taps(R) <= (others => '0');
				a_result(R) <= (others => '0');
			end loop;
			for P in a_past'range loop
				a_past(P) <= (others => '0');
			end loop;
			r_error <= (others => '0');
			
		elsif (rising_edge(i_clk)) then
			--First stage, let out result be 2*g_width!!
			for R in 1 to 7 loop
				a_result(R) <= a_taps(R) * a_past(R);
			end loop;
			a_result(0) <= a_taps(0) * i_refere;
			
			--Second stage
			for R in 0 to 7 loop
				v_sum := v_sum + resize(a_result(R), 2*g_width+3);
			end loop;	
			r_error <= i_contam - v_sum(2*g_width+3-1 downto g_width+3);
		
			--Third!
			for T in 0 to 7 loop
				v_errorDataProduct := r_error * a_past(T+2);
				a_taps(T) <= a_taps(T) + shift_left(v_errorDataProduct(g_width*2-1 downto g_width), g_mu);
			end loop;
			
			--Shift register of past values
			for T in 1 to 7+2 loop
				a_past(T) <= a_past(T-1);
			end loop;
			a_taps(0) <= i_refere;
		end if;
		wait;
	end process;

end arch;