public class Nano4T_Data
{
	public SubscribeableProperty<int> humanLayer;

	public SubscribeableProperty<int> nanoLayer;

	public SubscribeableProperty<int> pickUpBoxCount;

	private bool canUseGrave;

	private int graveCount;

	public int Layer_Human
	{
		get
		{
			return 0;
		}
		set
		{
		}
	}

	public int Layer_Nano
	{
		get
		{
			return 0;
		}
		set
		{
		}
	}

	public int Layer_Box
	{
		get
		{
			return 0;
		}
		set
		{
		}
	}

	public void Clear()
	{
	}

	public bool TryUseGrave()
	{
		return false;
	}

	public static int GetMaxCountOfBox(Player player)
	{
		return 0;
	}

	public void ClearBoxLayer()
	{
	}
}
