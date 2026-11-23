namespace Cheat
{
	public class RadioChild : ChoiceBase
	{
		public RadioChild(string name)
			: base(null)
		{
		}

		public override bool OnSelect()
		{
			return false;
		}

		public override bool GetFocus()
		{
			return false;
		}
	}
}
