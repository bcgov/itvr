using System;
using System.Management.Automation;

namespace pscoretest // Note: actual namespace depends on the project name.
{
    internal class Program
    {
        static void Main(string[] args)
        {
            using (PowerShell ps = PowerShell.Create())
            {
                var results = ps.AddScript("Get-Command").Invoke();


                foreach(var item in results)
                {
                    Console.WriteLine(item);
                }
            }
            Console.WriteLine("Hello World!");
        }
    }
}
