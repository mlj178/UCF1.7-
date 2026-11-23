using System;

namespace Cheat
{
	public class Function : ChoiceBase
	{
		private Action action;

		public Function(string name, Action action)
			: base(null)
		{
		}

		public override bool OnSelect()
		{
			return false;
		}
	}
}
