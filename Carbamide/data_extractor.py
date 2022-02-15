import os
import pandas as pd
import glob
from collections import OrderedDict


def check_opt(file):
    data = {}
    freq = False
    opt = False
    prevline = ""
    with open(file, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            line_duo = prevline + line
            line_duo = line_duo.replace("\n","")
            line_duo = line_duo.replace(" ","")
            if "    -- Stationary point found." in line:
                opt = True
            if "NImag=0" in line:
                freq = True
            if "NImag=0" in line_duo:
                freq = True
            prevline = line
        if opt and freq:
            return True
        else:
            return False
        
def gen_opt_names(pref, directory, nconf):
    opts = []
    dsds= []
    dats = []

    _cs = [".","_c2."]
    c = _cs[nconf]
    _solvent = ["_", "_Pentadecane_", "_water_"]
    dsds.append(directory+pref+c+"DSDPBEP86_AUG-cc-PVTZ.log")
    dats.append(directory+pref+c+"M062X_6-311pGd_opt_GD3.298.15.dat")
    for s in _solvent:
        opts.append(directory+pref+c+"M062X_6-311pGd_opt"+ s + "GD3.log")  
    return opts, dsds, dats

def get_M062X_E(fname):
    final_E = 0
    with open(fname, "r") as f:
        lines = f.readlines()
        for line in lines:
            if "SCF Done:  E(RM062X) =" in line:
                toks = line.split()
                final_E = float(toks[4])
    if final_E == 0:
        raise Exception ("no energy read")
    return final_E

def get_DSD_E(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
        for line in lines:
            if "E(DSDPBEP86) =" in line:
                toks = line.split()
                final_E = float(toks[5].replace("D", "E"))
    return final_E
                
def get_thermochem(fname):
    tchem = {}
    with open(fname, "r") as f:
        lines = f.readlines()
        for line in lines:
            if "ZPVE in kJ/mol" in line:
                toks = line.split()
                zpve = float(toks[4])
            if " TC Harmonic oscillator" in line:
                toks = line.split()
                tc = float(toks[4])
            if "Stotal Harmonic oscillator" in line:
                toks = line.split()
                Stotal = float(toks[4])
        if not (zpve or tc or Stotal):
            raise Exception
        tchem["ZPVE"] = zpve
        tchem["TC"] = tc
        tchem["S"] = Stotal
    return tchem

def ha_to_kJmol(ha):
    return 2625.50000000 *ha



nconfs = {}
nconfs["29"] = 2
nconfs["CP19"] = 2
nconfs["CP21"] = 1
nconfs["CP22"] = 2
nconfs["NM2"] = 2
nconfs["NM3"] = 2

data_df = pd.DataFrame()
prod_df = pd.DataFrame()
compounds = glob.glob("*/")
names_s_ls = []
for dir in ["29", "CP19","NM3", "CP21", "CP22", "NM2", ]:
    os.chdir(dir)
    print(os.getcwd())
    name_s = dir + "CA"
    names_s_ls.append(name_s)
    prev = 10000000
    prod_data = {}
    data = OrderedDict()
    data["Name"] = name_s

    print(f"NAME {name_s}")
    opt_names1, dsd_names1, dat_names1 = gen_opt_names("CA", dir,0)
        
    for opt_name in opt_names1:
        opt  = check_opt(opt_name)
        if not opt:
            raise Exception(f"{opt_name} not opt")
        else:
            name_print = opt_name.ljust(50, " ")
            print(f"{name_print} OPTIMISED and no IMAGINARY FREQ")
            eM062X = get_M062X_E(opt_name)
        if "water" in opt_name:
            water_1 = eM062X
        elif "Pentadecane" in opt_name:
            penta_1 = eM062X
        else:
            gas_1 = eM062X

        
    assert(len(dsd_names1) == 1)
    eDSD1 = get_DSD_E(dsd_names1[0])
    if eDSD1:
        dsd_print = dsd_names1[0].ljust(50, " ")
        print(f"{dsd_print} ENERGY FOUND")
    else:
        raise Exception

    assert(len(dat_names1) == 1)
    tchem1 = get_thermochem(dat_names1[0])
    if tchem1:
        print("TCHEM FOUND")
    else:
        raise Exception


    zpve_1  = tchem1["ZPVE"]
    tc_1 = tchem1["TC"]
    s_1 = tchem1["S"] / 1000 # to kJ
    ts_1 = s_1*298.15
    gsoln_gas_1 = ha_to_kJmol(eDSD1) + zpve_1 + tc_1 - ts_1 + 7.925291293  # include correct for standard state


    # check second conformer
    if nconfs[dir] == 2:
        opt_names2, dsd_names2, dat_names2 = gen_opt_names("CA", dir,1)
        
        for opt_name in opt_names2:
            opt  = check_opt(opt_name)
            if not opt:
                raise Exception(f"{opt_name} not opt")
            else:
                name_print = opt_name.ljust(50, " ")
                print(f"{name_print} OPTIMISED and no IMAGINARY FREQ")
                eM062X = get_M062X_E(opt_name)
            if "water" in opt_name:
                water_2 = eM062X
            elif "Pentadecane" in opt_name:
                penta_2 = eM062X
            else:
                gas_2 = eM062X

        
        assert(len(dsd_names2) == 1)
        eDSD2 = get_DSD_E(dsd_names2[0])
        if eDSD2:
            dsd_print = dsd_names2[0].ljust(50, " ")
            print(f"{dsd_print} ENERGY FOUND")
        else:
            raise Exception

        assert(len(dat_names2) == 1)
        tchem2 = get_thermochem(dat_names2[0])
        if tchem2:
            print("TCHEM FOUND")
        else:
            raise Exception


        zpve_2  = tchem2["ZPVE"]
        tc_2 = tchem2["TC"]
        s_2 = tchem2["S"] / 1000 # to kJ
        ts_2 = s_2*298.15
        gsoln_gas_2 = ha_to_kJmol(eDSD2) + zpve_2 + tc_2 - ts_2 + 7.925291293  # include correct for standard state

    # data_df = data_df.append(data, ignore_index=True)

        if gsoln_gas_1 < gsoln_gas_2:
            data["Gas M062X"] = gas_1
            data["Gas DSD"] = eDSD1
            data["ZPVE"] = zpve_1
            data["TC"] = tc_1
            data["S"] = s_1
            data["TS"] = ts_1
            data["GSoln Gas"] = gsoln_gas_1
        else:
            data["Gas M062X"] = gas_2
            data["Gas DSD"] = eDSD2
            data["ZPVE"] = zpve_2
            data["TC"] = tc_2
            data["S"] = s_2
            data["TS"] = ts_2
            data["GSoln Gas"] = gsoln_gas_2

        if water_1 < water_2:
            data["Water M062X"] = water_1
            data["DGSolv water"] =  ha_to_kJmol(water_1 - data["Gas M062X"]) 
            data["GSoln water"]  = data["GSoln Gas"] + data["DGSolv water"]
        
        else:
            data["Water M062X"] = water_2
            data["DGSolv water"] =  ha_to_kJmol(water_2 - data["Gas M062X"]) 
            data["GSoln water"]  = data["GSoln Gas"] + data["DGSolv water"]
        
        if penta_1 < penta_2:
            data["Penta M062X"] = penta_1
            data["DGSolv Penta"] =  ha_to_kJmol(penta_1 - data["Gas M062X"]) 
            data["GSoln Penta"]  = data["GSoln Gas"] + data["DGSolv Penta"]
        else:
            data["Penta M062X"] = penta_2
            data["DGSolv Penta"] =  ha_to_kJmol(penta_2 - data["Gas M062X"]) 
            data["GSoln Penta"]  = data["GSoln Gas"] + data["DGSolv Penta"]

    else:
        data["Gas M062X"] = gas_1
        data["Gas DSD"] = eDSD1
        data["ZPVE"] = zpve_1
        data["TC"] = tc_1
        data["S"] = s_1
        data["TS"] = ts_1
        data["GSoln Gas"] = gsoln_gas_1
        data["Water M062X"] = water_1
        data["DGSolv water"] =  ha_to_kJmol(water_1 - data["Gas M062X"]) 
        data["GSoln water"]  = data["GSoln Gas"] + data["DGSolv water"]
        data["Penta M062X"] = penta_1
        data["DGSolv Penta"] =  ha_to_kJmol(penta_1 - data["Gas M062X"]) 
        data["GSoln Penta"]  = data["GSoln Gas"] + data["DGSolv Penta"]


        
    data_df = data_df.append(data, ignore_index=True)

    os.chdir("../")


data_df = data_df.set_index("Name")
data_df = data_df[["Gas M062X", "Water M062X", "Penta M062X", "Gas DSD", "DGSolv water", "DGSolv Penta", "ZPVE", "TC", "S", "TS", "GSoln Gas", "GSoln water", "GSoln Penta"]]


print(data_df)
data_df.to_csv("DATA.csv")

