using System;

namespace Cheat
{
	public class Switch : ChoiceBase
	{
		private bool value;

		private Action<bool> action;

		public Switch(string name, Action<bool> action)
			: base(null)
		{
		}

		public override string GetText()
		{
			return null;
		}

		public override bool OnSelect()
		{
			return false;
		}
	}
}
